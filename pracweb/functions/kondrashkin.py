from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn.multiclass import OneVsRestClassifier

import numpy as np
import pylab as pl

from .common import Classifier
try:
  from pracweb.registry import classifier, corrector
except ImportError:
  classifier = lambda x: lambda y: y
  corrector = classifier


@classifier('naive_bayesian')
class NaiveBayesian(Classifier):
  def __init__(self, x_train, y_train):
    Classifier.__init__(self, GaussianNB(), x_train, y_train)
  def describe(self):
    pass

@classifier('linear_standard')
class LinearStandard(Classifier):
  def __init__(self, x_train, y_train):
    Classifier.__init__(self, LogisticRegression(fit_intercept=False), x_train, y_train)
  def describe(self):
    pass

@classifier('linear_affine')
class LinearAffine(Classifier):
  def __init__(self, x_train, y_train):
    Classifier.__init__(self, LogisticRegression(fit_intercept=True), x_train, y_train)
  def describe(self):
    pass

@classifier('linear_polynomial')
class LinearPolynomial(Classifier):
  def __init__(self, x_train, y_train):
    Classifier.__init__(self, SVC(kernel='poly', probability=True), x_train, y_train)
  def describe(self):
    pass

@classifier('decision_tree')
class DecisionTree(Classifier):
  def __init__(self, x_train, y_train):
    Classifier.__init__(self, DecisionTreeClassifier(), x_train, y_train)
  def describe(self):
    pass

@classifier('knn')
class KNN(Classifier):
  def __init__(self, x_train, y_train):
    Classifier.__init__(self, KNeighborsClassifier(n_neighbors=5, algorithm='brute'), x_train, y_train)
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

  clf = LinearAffine(x_train, y_train)

  y_pred = clf(x_test)
  y_pred = y_pred > 0.5

  pl.scatter(x_test[:,0], x_test[:,1], c=y_pred, alpha=0.3, s=100, marker='s')

  pl.scatter(x_test[:,0], x_test[:,1], c=y_test, alpha=0.7, s=50)

  pl.show()
