from collections import namedtuple
import numpy as np
import pracweb.registry as reg

Dataset = namedtuple('Dataset', 'learn test class_names')
Grid = namedtuple('Grid', 'left bottom right top width height')
Model = namedtuple('Model', 'classifiers corrector')
Problem = namedtuple('Problem', 'data model colormap grid')


def parse_request(data):
    return Problem(
        parse_objects(data['data']),
        parse_model(data['model']),
        parse_colors(data['colors']),
        parse_grid(data['grid']))


def parse_objects(data):
    ensure(isinstance(data, dict))
    ensure('learn' in data and 'test' in data)
    data_learn = data['learn']
    data_test = data['test']
    ensure(isinstance(data_learn, list))
    ensure(isinstance(data_test, list))
    ensure(len(data_learn) > 0, "learning dataset is empty")

    classes = set(obj['c'] for obj in data_learn)
    classes.update(obj['c'] for obj in data_test)
    ensure(all(isinstance(classname, basestring)
               for classname in classes))
    class_names = dict(enumerate(sorted(classes)))
    rev_class_names = dict((name, n)
                           for n, name
                           in class_names.iteritems())

    def make_np_data(objects):
        ensure(all('x' in obj and 'y' in obj and 'c' in obj
                   for obj in objects))
        return (
            np.array([(obj['x'], obj['y']) for obj in objects],
                     dtype=float),
            np.array([rev_class_names[obj['c']] for obj in objects],
                     dtype=int),
        )

    return Dataset(make_np_data(data_learn),
                   make_np_data(data_test),
                   class_names)


def parse_model(model):
    classifiers = model['classifiers']
    ensure(isinstance(classifiers, list) and classifiers,
           "no classifier selected")
    classifiers = set(classifiers)
    ensure(all(name in reg.classifiers for name in classifiers),
           "invalid classifier name")

    corrector = model['corrector']
    ensure(corrector in reg.correctors,
           "invalid corrector name")
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
