# vim: et sw=4
# encoding: utf-8

from sklearn.neighbors import KNeighborsClassifier
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

#Метод логарифмических шаров     Потапенко, Куракин, Огнева, Зак, Остапец

class LogarithmicBalls(Classifier):
    def __init__(self, x_train, y_train):
        Classifier.__init__(self, ProbaCentroid(), x_train, y_train)

@classifier('logarithmic_balls_potapenko')
class LogarithmicBallsPotapenko(LogarithmicBalls):
    description = {
        'name': u'Логарифмические шары',
        'author': u'А. Потапенко',
    }

@classifier('logarithmic_balls_kurakin')
class LogarithmicBallsKurakin(LogarithmicBalls):
    description = {
        'name': u'Логарифмические шары',
        'author': u'А. Куракин',
    }

@classifier('logarithmic_balls_ogneva')
class LogarithmicBallsOgneva(LogarithmicBalls):
    description = {
        'name': u'Логарифмические шары',
        'author': u'Д. Огнева',
    }
@classifier('logarithmic_balls_zak')
class LogarithmicBallsZak(LogarithmicBalls):
    description = {
        'name': u'Логарифмические шары',
        'author': u'Е. Зак',
    }
@classifier('logarithmic_balls_ostapetc')
class LogarithmicBallsOstapetc(LogarithmicBalls):
    description = {
        'name': u'Логарифмические шары',
        'author': u'А. Остапец',
    }

# Parzen in fact
class AVO(Classifier):
    def __init__(self, x_train, y_train, window_size=20):
        weights = lambda dists: np.float32(dists <= window_size) + 0.01
        Classifier.__init__(self, KNeighborsClassifier(n_neighbors=5000,
                weights=weights, algorithm='brute'), x_train, y_train)

@classifier('avo_nizhibitcky')
class AVONizhibitcky(AVO):
    description = {
        'name': u'АВО',
        'author': u'Е. Нижибицкий',
    }

@classifier('avo_morozova')
class AVOMorozova(AVO):
    description = {
        'name': u'АВО',
        'author': u'Д. Морозова',
    }

@classifier('avo_shaim')
class AVOShaim(AVO):
    description = {
        'name': u'АВО',
        'author': u'И. Шаймарданов',
    }

@classifier('avo_romov')
class AVORomov(AVO):
    description = {
        'name': u'АВО',
        'author': u'П. Ромов',
    }

@classifier('avo_ostap')
class AVOOstap(AVO):
    description = {
        'name': u'АВО',
        'author': u'А. Остапец',
    }

#@classifier('avo_gavr')
#class AVOGavr(AVO):
#    description = {
#        'name': u'АВО',
#        'author': u'М. Гавриков',
#    }

@classifier('avo_berezin')
class AVOBerezin(AVO):
    description = {
        'name': u'АВО',
        'author': u'А. Березин',
    }
