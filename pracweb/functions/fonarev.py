# vim: et sw=4
# encoding: utf-8
from sklearn.neighbors import KNeighborsClassifier

import numpy as np

from .common import Classifier
try:
    from pracweb.registry import classifier, corrector
except ImportError:
    classifier = lambda x: lambda y: y
    corrector = classifier


@classifier('parzen_finite')
class FiniteParzen(Classifier):
    def __init__(self, x_train, y_train, window_size=10):
        weights = lambda dists: np.float32(dists <= window_size) + 0.01
        Classifier.__init__(
            self,
            KNeighborsClassifier(n_neighbors=10000, weights=weights, algorithm='brute'),
            x_train,
            y_train)


@classifier('parzen_standard')
class StandardParzen(Classifier):
    def __init__(self, x_train, y_train, window_size=10):
        weights = lambda dists: np.exp(-dists ** 2 / window_size)
        Classifier.__init__(
            self,
            KNeighborsClassifier(n_neighbors=10000, weights=weights, algorithm='brute'),
            x_train,
            y_train)
