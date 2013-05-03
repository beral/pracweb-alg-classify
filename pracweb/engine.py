import os.path
import numpy as np
import ctypes
import Image

from . import registry
from . import native


def solve(problem):
    n_classes = len(problem.data.class_names)
    classifiers = [registry.classifiers[c](problem.data.learn[0],
                                           problem.data.learn[1])
                   for c in problem.model.classifiers]
    corrector = registry.correctors[problem.model.corrector](
        apply_classifiers(classifiers, problem.data.learn[0], n_classes),
        problem.data.learn[1],
        n_classes)
    return classifiers, corrector


def build_map(model, problem):
    classifiers, corrector = model
    n_classes = len(problem.data.class_names)
    Xgrid = make_grid(problem.grid)
    Kprobs = apply_classifiers(classifiers, Xgrid, n_classes)
    return corrector(Kprobs)


def make_grid(grid):
    xx = np.linspace(grid.left,
                     grid.right,
                     grid.width)
    yy = np.linspace(grid.top,
                     grid.bottom,
                     grid.height).T
    xx, yy = np.meshgrid(xx, yy)
    return np.c_[xx.ravel(), yy.ravel()]


def apply_classifiers(classifiers, x, n_classes):
    Kprobs = np.empty((x.shape[0], n_classes, len(classifiers)))
    for i in xrange(0, len(classifiers)):
        Kprobs[:, :, i] = classifiers[i](x)
    return Kprobs


def prepare_cmap(problem):
    n_classes = len(problem.data.class_names)
    cmap = np.empty((n_classes, 3))
    for c in xrange(0, n_classes):
        cmap[c, :] = problem.colormap[problem.data.class_names[c]]
    return cmap


def make_visuals(Fprobs, problem):
    cmap = prepare_cmap(problem)

    newimg = lambda: np.empty(
        (Fprobs.shape[0], 3),
        dtype=ctypes.c_uint8
    )
    toimg = lambda v: v.reshape((problem.grid.height, problem.grid.width, 3))

    viz_argmax = newimg()
    viz_intensity = newimg()
    viz_linspace = newimg()
    viz_linspace_clamped = newimg()
    viz_diff = newimg()

    native.visualize(
        Fprobs.shape[0],
        Fprobs.shape[1],
        Fprobs,
        cmap,
        np.empty((Fprobs.shape[0], 2), dtype=ctypes.c_size_t),  # argmaxs
        np.empty(Fprobs.shape[1], dtype=ctypes.c_double),  # diff_norms
        np.empty(Fprobs.shape[1], dtype=ctypes.c_double),  # ks
        viz_argmax,
        viz_intensity,
        viz_linspace,
        viz_linspace_clamped,
        viz_diff,
    )

    return {
        'argmax': toimg(viz_argmax),
        'intensity': toimg(viz_intensity),
        'linspace': toimg(viz_linspace),
        'linspace_clamped': toimg(viz_linspace_clamped),
        'diff': toimg(viz_diff),
    }


def store_images(images, task_id, store_path):
    if not os.path.isdir(store_path):
        os.mkdir(store_path)

    paths = dict()
    for name, imgbuf in images.iteritems():
        Image.fromarray(imgbuf).save(os.path.join(
            store_path,
            '{0}_{1}.png'.format(task_id, name)))
        paths[name] = 'result/{0}/{1}.png'.format(task_id, name)
    return paths
