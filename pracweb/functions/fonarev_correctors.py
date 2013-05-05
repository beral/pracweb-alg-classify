import numpy as np
from copy import deepcopy
from pybrain.optimization import CMAES
from copy import deepcopy
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
    def __init__(self, x_learn, y_learn):
        _, y = nclass_to_nbinary(y_learn)
        x = deepcopy(x_learn)
        self.weights = np.array([])

        for oper_number in range(1, x.shape[2] + 1):
            func_min = 100000
            func_argmin = 0

            for new_weight in np.arange(0, 5, 0.01):
                w = np.hstack([self.weights, new_weight])
                func_value = \
                        np.sum((np.dot(x[:, :, :oper_number], w) - y) ** 2)
                if func_value < func_min:
                    func_min, func_argmin = func_value, new_weight

            self.weights = np.hstack([self.weights, func_argmin])

    def __call__(self, x_val):
        print >> sys.stderr, "x size", x_val.shape
        print >> sys.stderr, "weights size", self.weights.shape
        print >> sys.stderr, "weights: ", self.weights

        return np.dot(x_val, self.weights)

@corrector("unstable_monotone_linear")
class UnstableMonotoneLinear(object):
    def __init__(self, x_learn, y_learn):
        _, y = nclass_to_nbinary(y_learn)
        x = np.swapaxes(x_learn, 1, 2)
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

        return np.dot(np.swapaxes(x_val, 1, 2), self.weights)

if __name__ == '__main__':
    x_learn = np.round(np.random.random([5, 4, 3]) * 5)
    print x_learn
    y_learn = np.array([1,2,3,4,1])
    x_test = np.round(np.random.random([5, 4, 3]) * 5)

    c = MonotoneLinear(x_learn, y_learn)
    print c.weights
    print c(x_test)
