# vim: et sw=4
# encoding: utf-8
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split

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


# NOT FINISHED!
#@corrector("monotone_affine")
class MonotoneAffine(object):
    def __init__(self, estimates, labels):
        self.clf_list = []
        for label_number in range(estimates.shape[2]):
            current_clf = LogisticRegression(fit_intercept=True)
            current_clf.fit(estimates[:, :, label_number], labels[:, label_number])
            self.clf_list.append(current_clf)

    def __call__(self, estimates):
        labels = np.zeros([estimates.shape[0], estimates.shape[2]])
        for label_number in range(estimates.shape[2]):
            labels[:, label_number] = \
                self.clf_list[label_number].predict_proba(estimates[:, :, label_number])[1]
            return labels


def test_iris():
    from sklearn.datasets import load_iris
    iris = load_iris()
    X, y = iris.data, iris.target
    X = X[:, [0, 2]]
    x_train, x_test, y_train, y_test = train_test_split(X, y)
    return x_train, x_test, y_train, y_test


def run_test():
    import pylab as pl
    x_train, x_test, y_train, y_test = test_iris()

    clf = FiniteParzen(x_train, y_train)
    #clf = StandartParzen(x_train, y_train)

    y_pred = clf(x_test)
    y_pred = y_pred > 0.5

    pl.scatter(x_test[:, 0], x_test[:, 1],
               c=y_pred, alpha=0.3, s=100, marker='s')

    pl.scatter(x_test[:, 0], x_test[:, 1],
               c=y_test, alpha=0.7, s=50)

    pl.show()


if __name__ == '__main__':
    run_test()
