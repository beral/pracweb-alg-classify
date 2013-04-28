from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split

import numpy as np
import pylab as pl

from .common import Classifier
try:
  from pracweb.registry import classifier, corrector
except ImportError:
  classifier = lambda x: lambda y: y
  corrector = classifier


@classifier('parzen_finite')
class FiniteParzen(Classifier):
  def __init__(self, x_train, y_train, window_size=10):
    weights = lambda dists: np.float32(dists <= window_size)
    Classifier.__init__(self, KNeighborsClassifier(n_neighbors=10000,
            weights=weights, algorithm='brute'), x_train, y_train)
  def describe(self):
    pass

@classifier('parzen_standard')
class StandardParzen(Classifier):
  def __init__(self, x_train, y_train, window_size=10):
    weights = lambda dists: np.exp(-dists ** 2 / window_size)
    Classifier.__init__(self, KNeighborsClassifier(n_neighbors=10000,
            weights=weights, algorithm='brute'), x_train, y_train)
  def describe(self):
    pass

def test_iris():
  from sklearn.datasets import load_iris
  iris = load_iris()
  X, y = iris.data, iris.target
  X = X[:,[0,2]]
  x_train, x_test, y_train, y_test = train_test_split(X, y)
  return x_train, x_test, y_train, y_test

if __name__ == '__main__':
  x_train, x_test, y_train, y_test = test_iris()

  clf = FiniteParzen(x_train, y_train)
  #clf = StandartParzen(x_train, y_train)

  y_pred = clf(x_test)
  y_pred = y_pred > 0.5

  pl.scatter(x_test[:,0], x_test[:,1], c=y_pred, alpha=0.3, s=100, marker='s')

  pl.scatter(x_test[:,0], x_test[:,1], c=y_test, alpha=0.7, s=50)

  pl.show()
