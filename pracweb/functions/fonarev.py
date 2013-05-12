# vim: et sw=4
# encoding: utf-8
from sklearn.neighbors import KNeighborsClassifier

import numpy as np
import sys
from copy import deepcopy

from .common import Classifier
try:
    from pracweb.registry import classifier, corrector
except ImportError:
    classifier = lambda x: lambda y: y
    corrector = classifier

@classifier('parzen_finite')
class FiniteParzen(Classifier):
    description = {'author': u'А. Фонарев', 'name': u'Парзеновский АО с финитным окном'}

    def __init__(self, x_train, y_train, window_size=20):
        self.window_size = window_size
        weights = lambda dists: np.float32(dists <= window_size) + 0.01
        Classifier.__init__(
            self,
            KNeighborsClassifier(n_neighbors=10000, weights=weights, algorithm='brute'),
            x_train,
            y_train)

    def describe(self):
        return {'window_size': self.window_size}

@classifier('parzen_standard')
class StandardParzen(Classifier):
    description = {'author': u'А. Фонарев', 'name': u'Стандартный парзеновский АО'}

    def __init__(self, x_train, y_train, window_size=20):
        self.window_size = window_size
        weights = lambda dists: np.exp(-dists ** 2 / window_size)
        Classifier.__init__(
            self,
            KNeighborsClassifier(n_neighbors=10000, weights=weights, algorithm='brute'),
            x_train,
            y_train)

    def describe(self):
        return {'window_size': self.window_size}

if __name__ == '__main__':
    x_learn = np.round(np.random.random([3,5,4]) * 5)
    y_learn = np.round(np.random.random([3,4]) * 5)
    x_test = np.round(np.random.random([3,5,4]) * 5)

    c = MonotoneLinear(x_learn, y_learn)
    print c.weights
    print c(x_test)
