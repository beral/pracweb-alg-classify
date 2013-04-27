from collections import namedtuple
import numpy as np
import pracweb.registry as reg

Dataset = namedtuple('Dataset', 'learn control class_names')
Grid = namedtuple('Grid', 'left bottom right top width height')
Model = namedtuple('Model', 'classifiers corrector')
Problem = namedtuple('Problem', 'data model colormap grid')


def parse_request(data):
    return Problem(
        parse_objects(data['objects']),
        parse_model(data['model']),
        parse_colors(data['colors']),
        parse_grid(data['grid']))


def parse_objects(objects):
    ensure(isinstance(objects, list))
    n = len(objects)
    ensure(n > 0, "object list is empty")

    classes = set(obj['c'] for obj in objects)
    ensure(all(isinstance(classname, basestring) for classname in classes))
    class_names = dict(enumerate(sorted(classes)))
    rev_class_names = dict((name, n) for n, name in class_names.iteritems())

    learn = []
    control = []
    for obj in objects:
        desc = (obj['x'], obj['y'], rev_class_names[obj['c']])
        if obj['t']:
            learn.append(desc)
        else:
            control.append(desc)

    n_learn = (
        np.array([(x, y) for x, y, _ in learn], dtype=float),
        np.array([c for _, _, c in learn], dtype=int),
    )
    n_control = (
        np.array([(x, y) for x, y, _ in control], dtype=float),
        np.array([c for _, _, c in control], dtype=int),
    )

    return Dataset(n_learn, n_control, class_names)


def parse_model(model):
    classifiers = model['classifiers']
    ensure(isinstance(classifiers, list) and classifiers,
           "empty classifier list")
    classifiers = set(classifiers)
    ensure(all(name in reg.classifiers for name in classifiers),
           "invalid classifier name")

    corrector = model['corrector']
    ensure(corrector in reg.correctors, "invalid corrector name")
    return Model(classifiers, corrector)


def parse_colors(colors):
    ensure(isinstance(colors, dict))
    colormap = dict()
    for classname, color in colors.iteritems():
        ensure(isinstance(classname, basestring))
        r, g, b = map(float, color)
        colormap[classname] = (r, g, b)
    return colormap


def parse_grid(grid):
    left, top, right, bottom = [float(grid[x]) for x in ('left', 'top', 'right', 'bottom')]
    width, height = [int(grid[x]) for x in ('width', 'height')]
    return Grid(left, bottom, right, top, width, height)


def ensure(stmt, message="unknown error"):
    if not stmt:
        raise ValueError(message)
