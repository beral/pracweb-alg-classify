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

class FiniteParzen(Classifier):
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

@classifier('parzen_finite_ismagilov')
class FiniteParzenIsmagilov(FiniteParzen):
    description = {'author': u'Т. Исмагилов', 'name': u'Парзеновский АО с финитным окном'}

@classifier('parzen_finite_zak')
class FiniteParzenZak(FiniteParzen):
    description = {'author': u'Е. Зак', 'name': u'Парзеновский АО с финитным окном'}

@classifier('parzen_finite_morozova')
class FiniteParzenMorozova(FiniteParzen):
    description = {'author': u'Д. Морозова', 'name': u'Парзеновский АО с финитным окном'}

class StandardParzen(Classifier):
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

@classifier('parzen_standard_kurakin')
class StandardParzenKurakin(StandartParzen):
    description = {'author': u'А. Куракин', 'name': u'Стандартный парзеновский АО'}

@classifier('parzen_standard_novikov')
class StandardParzenNovikov(StandartParzen):
    description = {'author': u'М. Новиков', 'name': u'Стандартный парзеновский АО'}

if __name__ == '__main__':
    x_learn = np.round(np.random.random([3,5,4]) * 5)
    y_learn = np.round(np.random.random([3,4]) * 5)
    x_test = np.round(np.random.random([3,5,4]) * 5)

    c = MonotoneLinear(x_learn, y_learn)
    print c.weights
    print c(x_test)
