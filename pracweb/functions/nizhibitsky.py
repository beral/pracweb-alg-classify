# vim: et sw=4
# encoding: utf-8

from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.cross_validation import train_test_split

import numpy as np
import pylab as pl

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
    def __init__(self, x_train, y_train):
        Classifier.__init__(self, ProbaCentroid(), x_train, y_train)


# TO BE DONE!!!
#@classifier('avo')
class AVO(Classifier):
    def __init__(self, x_train, y_train):
        Classifier.__init__(self, KNeighborsClassifier(n_neighbors=5, algorithm='brute'), x_train, y_train)


def test_iris():
    from sklearn.datasets import load_iris
    iris = load_iris()
    X, y = iris.data, iris.target
    X = X[:, [0, 2]]
    x_train, x_test, y_train, y_test = train_test_split(X, y)
    return x_train, x_test, y_train, y_test


def run_test():
    x_train, x_test, y_train, y_test = test_iris()

    clf = LogarithmicBalls(x_train, y_train)
    #clf = AVO(x_train, y_train)

    y_pred = clf(x_test)
    y_pred = y_pred > 0.5

    #pl.scatter(x_test[:, 0], x_test[:, 1],
    #           c=y_pred, alpha=1.0, s=200, marker='s')

    pl.scatter(x_test[:, 0], x_test[:, 1],
               c=y_pred, alpha=1.0, s=50)

    pl.show()


if __name__ == '__main__':
    run_test()
