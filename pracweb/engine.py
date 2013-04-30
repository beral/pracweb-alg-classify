import numpy as np
import Image
from celery import Celery

import pracweb.registry as reg

celery = Celery("engine",
                broker='redis://localhost:6379/0',
                backend='redis')


class ImagePack(object):
    def __init__(self, array):
        self.array = array

    def unpack(self):
        return Image.fromarray(self.array)


@celery.task
def process_problem(problem):
    chain = (solve.s(problem)
             | build_map.s(problem)
             | make_visuals.s(problem)
             | assemble_result.s())
    return chain().get()


@celery.task
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


@celery.task
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


@celery.task
def make_visuals(Fprobs, problem):
    cmap = prepare_cmap(problem)

    newimg = lambda: np.empty((Fprobs.shape[0], 3), dtype=np.uint8)
    toimg = lambda v: ImagePack(
        Image.fromarray(
            v.reshape(
                (problem.grid.height, problem.grid.width, 3)
            )
        )
    )

    viz_argmax = newimg()
    viz_intensity = newimg()
    viz_linspace = newimg()
    viz_linspace_clamped = newimg()
    viz_diff = newimg()

    p_max = np.max(Fprobs)
    p_min = np.min(Fprobs)
    argmaxs = np.empty((Fprobs.shape[0], 2), dtype=int)
    diff_norms = np.zeros(Fprobs.shape[1])
    for x in xrange(0, Fprobs.shape[0]):
        order = np.argsort(Fprobs[x, :])
        c, c2 = order[-1], order[-2]
        argmaxs[x, :] = c, c2
        diff_norms[c] = max(diff_norms[c], Fprobs[x, c] - Fprobs[x, c2])

    viz_argmax[:, :] = cmap[argmaxs[:, 0], :]
    #kss = (Fprobs - p_min) / (p_max - p_min + 1e-5)
    #viz_intensity[:, :] = np.dot(kss[:, argmaxs[:, 0]], cmap[argmaxs[:, 0], :])
    for x in xrange(0, Fprobs.shape[0]):
        c, c2 = argmaxs[x, :]
        ks = (Fprobs[x, :] - p_min) / (p_max - p_min + 1e-5)
        #viz_argmax[x, :] = cmap[c, :]
        viz_intensity[x, :] = ks[c] * cmap[c, :]
        viz_linspace[x, :] = np.dot(ks / sum(ks), cmap)
        viz_linspace_clamped[x, :] = np.clip(np.dot(ks, cmap), 0, 255)
        viz_diff[x, :] = cmap[c, :] * ((Fprobs[x, c] - Fprobs[x, c2]) / diff_norms[c])

    return {
        'argmax': toimg(viz_argmax),
        'intensity': toimg(viz_intensity),
        'linspace': toimg(viz_linspace),
        'linspace_clamped': toimg(viz_linspace_clamped),
        'diff': toimg(viz_diff),
    }


@celery.task
def assemble_result(visuals):
    return {
        'visuals': visuals
    }
