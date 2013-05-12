# vim: et sw=4
# encoding: utf-8

from sklearn.neighbors import NearestCentroid
from sklearn.metrics.pairwise import pairwise_distances

import numpy as np

from .common import Classifier
try:
    from pracweb.registry import classifier, corrector
except ImportError:
    classifier = lambda x: lambda y: y
    corrector = classifier


class ProbaCentroid(NearestCentroid):
    def __init__(self):
        self.metric = lambda x1, x2: np.log(np.sqrt(np.sum(np.square(x1 - x2))))
        NearestCentroid.__init__(self, metric=self.metric)

    def predict_proba(self, X):
        if not hasattr(self, "centroids_"):
            raise AttributeError("Model has not been trained yet.")
        dists = pairwise_distances(X, self.centroids_, metric=self.metric)
        sums = np.sum(dists, axis=1)
        return 1 - np.divide(dists,
                             np.reshape(np.repeat(sums, 2),
                                        dists.shape))


@classifier('logarithmic_balls')
class LogarithmicBalls(Classifier):
    description = {
        'name': u'Логарифмические шары',
        'author': u'Е. Нижибицкий',
    }

    def __init__(self, x_train, y_train):
        Classifier.__init__(self, ProbaCentroid(), x_train, y_train)
