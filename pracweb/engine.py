import numpy as np
import ctypes
import Image
from celery import Celery

import pracweb.registry as reg
import pracweb.native as native

celery = Celery("engine",
                broker='redis://localhost:6379/0',
                backend='redis')


class ImagePack(object):
    def __init__(self, array):
        self.array = array

    def unpack(self):
        return Image.fromarray(self.array)


@celery.task(track_started=True, acks_late=True)
def process_problem(problem):
    model = solve(problem)
    estimate_map = build_map(model, problem)
    return {
        'visuals': make_visuals(estimate_map, problem)
    }


def solve(problem):
    n_classes = len(problem.data.class_names)
    classifiers = [reg.classifiers[c](problem.data.learn[0],
                                      problem.data.learn[1])
                   for c in problem.model.classifiers]
    corrector = reg.correctors[problem.model.corrector](
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
    toimg = lambda v: ImagePack(
        v.reshape(
            (problem.grid.height, problem.grid.width, 3)
        )
    )

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
