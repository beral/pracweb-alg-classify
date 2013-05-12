# vim: et sw=4
# encoding: utf-8

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression

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


@classifier('linear_standard')
class LinearStandard(Classifier):
    def __init__(self, x_train, y_train):
        Classifier.__init__(self, LogisticRegression(fit_intercept=False), x_train, y_train)


@classifier('linear_affine')
class LinearAffine(Classifier):
    def __init__(self, x_train, y_train):
        Classifier.__init__(self, LogisticRegression(fit_intercept=True), x_train, y_train)


@classifier('linear_polynomial')
class LinearPolynomial(Classifier):
    def __init__(self, x_train, y_train):
        Classifier.__init__(self, SVC(kernel='poly', probability=True), x_train, y_train)


@classifier('decision_tree')
class DecisionTree(Classifier):
    def __init__(self, x_train, y_train):
        Classifier.__init__(self, DecisionTreeClassifier(max_depth=1), x_train, y_train)


@classifier('knn')
class KNN(Classifier):
    def __init__(self, x_train, y_train):
        Classifier.__init__(self, KNeighborsClassifier(n_neighbors=5, algorithm='brute'), x_train, y_train)
