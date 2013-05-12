# -*- coding: utf-8 -*-

import numpy as np
from pybrain.optimization import CMAES
import sys

try:
    from pracweb.registry import classifier, corrector
except ImportError:
    # Dummies
    classifier = lambda x: lambda y: y
    corrector = classifier

def nclass_to_nbinary(y):
    print y
    dim = len(set(y))
    flags = np.zeros((y.size, dim))
    for i, c in enumerate(y):
        flags[i, c - 1] = 1
    return dim, flags

@corrector("monotone_linear")
class MonotoneLinear(object):
    description = {'author': u'А. Фонарев', 'name': u'Монотонная линейная КО'}
    def __init__(self, x_learn, y_learn):
        _, y = nclass_to_nbinary(y_learn)
        x = x_learn
        x, y = x - 0.5, y - 0.5
        self.weights = np.array([])

        for oper_number in range(1, x.shape[2] + 1):
            func_min = 100000
            func_argmin = 0

            for new_weight in np.arange(0, 2, 0.01):
                w = np.hstack([self.weights, new_weight])
                predicted = np.dot(x[:, :, :oper_number], w)
                predicted[predicted > 0.5] = 0.5
                predicted[predicted < -0.5] = -0.5
                func_value = np.sum((predicted - y) ** 2)
                if func_value < func_min:
                    func_min, func_argmin = func_value, new_weight

            self.weights = np.hstack([self.weights, func_argmin])

    def __call__(self, x_val):
        print >> sys.stderr, "x size", x_val.shape
        print >> sys.stderr, "weights size", self.weights.shape
        print >> sys.stderr, "weights: ", self.weights

        result = np.dot(x_val - 0.5, self.weights) + 0.5
        result[result > 1] = 1
        result[result < 0] = 0
        return result

    def describe(self):
        return {'weights': list(self.weights)}

@corrector("monotone_affine")
class MonotoneAffine(object):
    description = {'author': u'А. Фонарев', 'name': u'Монотонная аффинная КО'}
    def __init__(self, x_learn, y_learn):
        _, y = nclass_to_nbinary(y_learn)
        x = np.dstack([np.ones(x_learn.shape[0:1]), x_learn])
        x, y = x - 0.5, y - 0.5
        self.weights = np.array([])

        for oper_number in range(1, x.shape[2] + 1):
            func_min = 100000
            func_argmin = 0

            for new_weight in np.arange(0, 2, 0.01):
                w = np.hstack([self.weights, new_weight])
                predicted = np.dot(x[:, :, :oper_number], w)
                predicted[predicted > 0.5] = 0.5
                predicted[predicted < -0.5] = -0.5
                func_value = np.sum((predicted - y) ** 2)
                if func_value < func_min:
                    func_min, func_argmin = func_value, new_weight

            self.weights = np.hstack([self.weights, func_argmin])

    def __call__(self, x_val):
        print >> sys.stderr, "x size", x_val.shape
        print >> sys.stderr, "weights size", self.weights.shape
        print >> sys.stderr, "weights: ", self.weights

        x = np.dstack([np.ones(x_val.shape[0:1]), x_val])
        result = np.dot(x - 0.5, self.weights) + 0.5
        result[result > 1] = 1
        result[result < 0] = 0
        return result

    def describe(self):
        return {'weights': list(self.weights)}

@corrector("special_affine")
class SpecialAffine(object):
    description = {'author': u'А. Фонарев', 'name': u'Специальная аффинная КО'}
    def __init__(self, x_learn, y_learn):
        _, y = nclass_to_nbinary(y_learn)
        x = x_learn
        x, y = x - 0.5, y - 0.5
        self.weights = np.array([1])

        for oper_number in range(2, x.shape[2] + 1):
            func_min = 100000
            func_argmin = 0

            for new_weight in np.arange(-2, 2, 0.01):
                w = np.hstack([self.weights, new_weight])
                predicted = np.dot(x[:, :, :oper_number], w)
                predicted[predicted > 0.5] = 0.5
                predicted[predicted < -0.5] = -0.5
                func_value = np.sum((predicted - y) ** 2)

                if func_value < func_min:
                    func_min, func_argmin = func_value, new_weight

            self.weights = np.hstack([self.weights, func_argmin])

    def __call__(self, x_val):
        print >> sys.stderr, "x size", x_val.shape
        print >> sys.stderr, "weights size", self.weights.shape
        print >> sys.stderr, "weights: ", self.weights

        result = np.dot(x_val - 0.5, self.weights) + 0.5
        result[result > 1] = 1
        result[result < 0] = 0
        return result

    def describe(self):
        return {'weights': list(self.weights)}

@corrector("special_monotone_affine")
class SpecialMonotoneAffine(object):
    description = {'author': u'А. Фонарев', 'name': u'Специальная монотонная аффинная КО'}
    def __init__(self, x_learn, y_learn):
        _, y = nclass_to_nbinary(y_learn)
        x = x_learn
        x, y = x - 0.5, y - 0.5
        self.weights = np.array([1])

        for oper_number in range(2, x.shape[2] + 1):
            func_min = 100000
            func_argmin = 0

            for new_weight in np.arange(0, 2, 0.01):
                w = np.hstack([self.weights, new_weight])
                predicted = np.dot(x[:, :, :oper_number], w)
                predicted[predicted > 0.5] = 0.5
                predicted[predicted < -0.5] = -0.5
                func_value = np.sum((predicted - y) ** 2)

                if func_value < func_min:
                    func_min, func_argmin = func_value, new_weight

            self.weights = np.hstack([self.weights, func_argmin])

    def __call__(self, x_val):
        print >> sys.stderr, "x size", x_val.shape
        print >> sys.stderr, "weights size", self.weights.shape
        print >> sys.stderr, "weights: ", self.weights

        result = np.dot(x_val - 0.5, self.weights) + 0.5
        result[result > 1] = 1
        result[result < 0] = 0
        return result

    def describe(self):
        return {'weights': list(self.weights)}

class UnstableMonotoneLinear(object):
    def __init__(self, x_learn, y_learn):
        _, y = nclass_to_nbinary(y_learn)
        #x = np.swapaxes(x_learn, 1, 2)
        w = np.random.randn(np.shape(x)[2])
        print "x size", x.shape
        print "y size", y.shape

        func = lambda w: np.sum((np.dot(x, w) - y) ** 2) \
                + 10000 * np.sum(np.float32(w < 0)) \
                + np.sum(w ** 2)

        self.weights = np.random.randn(np.shape(x)[2])
        print "weights size", self.weights.shape
        optimizer = CMAES(func, self.weights)
        optimizer.minimize = True
        self.weights = optimizer.learn()[0]

    def __call__(self, x_val):
        print "x size", x_val.shape
        print "weights size", self.weights.shape

        return np.dot(x_val, self.weights)

if __name__ == '__main__':
    x_learn = np.round(np.random.random([5, 4, 3]) * 5)
    print x_learn
    y_learn = np.array([1,2,3,4,1])
    x_test = np.round(np.random.random([5, 4, 3]) * 5)

    c = MonotoneAffine(x_learn, y_learn)
    print c.weights
    print c(x_test)
