# -*- coding: utf-8 -*-

import yaml
import numpy as np
import ctypes
import sklearn.metrics as skm

from . import registry
from . import native


def solve(problem):
    '''Построить модель'''

    def make_sample(data):
        indexes = np.random.permutation(data[0].shape[0])
        indexes = indexes[:len(indexes) / 2 + 1]
        x_new = data[0][indexes, :]
        y_new = data[1][indexes]

        return x_new, y_new

    def make_balanced_sample(data):
        x = data[0]
        y = data[1]
        x_result = np.empty([0, data[0].shape[1]])
        y_result = np.empty([0])

        for class_number in np.unique(y):
            indexes = y == class_number
            x_class = x[indexes, :]
            y_class = y[indexes, :]
            x_class, y_class = make_sample((x_class, y_class))
            x_result = np.vstack([x_result, x_class])
            y_result = np.hstack([y_result, y_class])

        return x_result, y_result

    n_classes = len(problem.data.class_names)

    classifiers = []
    for c in problem.model.classifiers:
        sample = make_balanced_sample(problem.data.learn)
        classifiers.append(registry.classifiers[c](sample[0], sample[1]))

    # TODO: use all correctors, not [0]
    corrector = registry.correctors[problem.model.correctors[0]](
        apply_model(
            (classifiers, None),
            problem.data.learn[0],
            n_classes),
        problem.data.learn[1])

    return classifiers, corrector


def describe_model(model):
    '''Получить текстовое описание модели'''

    def describe(x):
        result = dict(meta=None, params=None)
        if hasattr(x, 'description'):
            result['meta'] = x.description
        if hasattr(x, 'describe'):
            result['params'] = x.describe()
        return result

    if callable(model):
        #return describe(model)
        return "go away, desu~"
    else:
        classifiers, corrector = model
        return yaml.safe_dump(describe(corrector), allow_unicode=True, default_flow_style=False)
        #model_params = dict(
        #    classifiers=[describe(x) for x in classifiers],
        #    corrector=describe(corrector))
        #return yaml.safe_dump(model_params, allow_unicode=True, default_flow_style=False)


def build_map(model, problem):
    '''Применить модель к двухмерной карте'''

    n_classes = len(problem.data.class_names)
    Xgrid = make_grid(problem.grid)
    Kprobs = apply_model(model, Xgrid, n_classes)
    return Kprobs


# TODO: (test, learn, learn+test)
def eval_model(model, problem):
    '''Оценить модель на прецедентах'''
    class_names = problem.data.class_names
    n_classes = len(class_names)
    Fprobs = apply_model(model, problem.data.test[0], n_classes)
    y_true = problem.data.test[1]
    y_pred = np.argmax(Fprobs, 1)
    labels = range(0, n_classes)

    metrics = skm.precision_recall_fscore_support(y_true, y_pred, labels=labels)
    confusion_matrix = skm.confusion_matrix(y_true, y_pred, labels)
    precision, recall, fscore, support = metrics

    metrics_data = [['',
                     'Precision',
                     'Recall',
                     'F-Score',
                     'Support']]
    for i in labels:
        metrics_data.append([
            class_names[i],
            precision[i],
            recall[i],
            fscore[i],
            int(support[i]),  # workaround: make json-serializable
        ])

    conf_data = [[''] + map(class_names.__getitem__, labels)]
    for i in labels:
        conf_data.append([class_names[i]] + confusion_matrix[i, :].tolist())

    return metrics_data, conf_data


def make_grid(grid):
    '''Создать набор объектов для двухмерной карты'''
    xx = np.linspace(grid.left,
                     grid.right,
                     grid.width)
    yy = np.linspace(grid.top,
                     grid.bottom,
                     grid.height).T
    xx, yy = np.meshgrid(xx, yy)
    return np.c_[xx.ravel(), yy.ravel()]


def apply_model(model, x, n_classes):
    '''Применить модель к данным.

    x - (n x 2) матрица данных
    model - ([classifiers], corrector) ИЛИ classifier
    '''

    if callable(model):
        Kprobs = model(x)
        return Kprobs
    else:
        classifiers, corrector = model
        Kprobs = np.empty((x.shape[0], n_classes, len(classifiers)))
        for i in xrange(0, len(classifiers)):
            Kprobs[:, :, i] = classifiers[i](x)
        if corrector:
            return corrector(Kprobs)
        else:
            return Kprobs


def prepare_cmap(problem):
    '''Преобразовать карту цветов к матрице'''

    n_classes = len(problem.data.class_names)
    cmap = np.empty((n_classes, 3))
    for c in xrange(0, n_classes):
        cmap[c, :] = problem.colormap[problem.data.class_names[c]]
    return cmap


def make_visuals(Fprobs, problem):
    '''Построить двухмерные диаграммы классификации'''

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
        np.array(Fprobs, order='C'),
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
