# -*- coding: utf-8 -*-

import numpy as np
from pybrain.optimization import CMAES
import sys

try:
    from pracweb.registry import classifier, corrector
except ImportError:
    # Dummies
    classifier = lambda x: lambda y: y
    corrector = classifier

def convert(y):
    dim = len(set(y))
    flags = np.zeros((0, dim))
    for c in y:
        flags = np.vstack([flags, np.zeros([1, dim])])
        flags[-1, c] = 1
    return dim, flags

def get_quality(real, predicted):
    result = 0
    for i in range(real.shape[0]):
        current_class = int(np.where(real[i, :] != 0)[0])
        result -= np.log(predicted[i, current_class] + 0.000001)
    return result

class MonotoneLinear(object):
    def __init__(self, x_learn, y_learn):
        _, y = convert(y_learn)
        x = x_learn
        x, y = x - 0.5, y - 0.5
        self.weights = np.array([])

        for oper_number in range(1, x.shape[2] + 1):
            func_min = 100000
            func_argmin = 0

            for new_weight in np.arange(0, 2, 0.01):
                w = np.hstack([self.weights, new_weight])
                predicted = np.dot(x[:, :, :oper_number], w)
                predicted[predicted > 0.5] = 0.5
                predicted[predicted < -0.5] = -0.5
                func_value = get_quality(y + 0.5, predicted + 0.5)
                if func_value < func_min:
                    func_min, func_argmin = func_value, new_weight

            self.weights = np.hstack([self.weights, func_argmin])

    def __call__(self, x_val):
        print >> sys.stderr, "x size", x_val.shape
        print >> sys.stderr, "weights size", self.weights.shape
        print >> sys.stderr, "weights: ", self.weights

        result = np.dot(x_val - 0.5, self.weights) + 0.5
        result[result > 1] = 1
        result[result < 0] = 0
        return result

    def describe(self):
        return {'weights': map(float, self.weights)}

@corrector("monotone_linear_potapenko")
class MonotoneLinearPotapenko(MonotoneLinear):
    description = {'author': u'А. Потапенко', 'name': u'Монотонная линейная КО'}

@corrector("monotone_linear_zak")
class MonotoneLinearZak(MonotoneLinear):
    description = {'author': u'Е. Зак', 'name': u'Монотонная линейная КО'}

@corrector("monotone_linear_malysheva")
class MonotoneLinearMalysheva(MonotoneLinear):
    description = {'author': u'Е. Малышева', 'name': u'Монотонная линейная КО'}

@corrector("monotone_linear_kondrashkin")
class MonotoneLinearKondrashkin(MonotoneLinear):
    description = {'author': u'Д. Кондрашкин', 'name': u'Монотонная линейная КО'}

@corrector("monotone_linear_gavrikov")
class MonotoneLinearGavrikov(MonotoneLinear):
    description = {'author': u'М. Гавриков', 'name': u'Монотонная линейная КО'}

@corrector("monotone_linear_morozovа")
class MonotoneLinearMorozova(MonotoneLinear):
    description = {'author': u'Д. Морозова', 'name': u'Монотонная линейная КО'}

@corrector("monotone_linear_shaimardanov")
class MonotoneLinearShaimardanov(MonotoneLinear):
    description = {'author': u'И. Шаймарданов', 'name': u'Монотонная линейная КО'}

@corrector("monotone_linear_kurakin")
class MonotoneLinearKurakin(MonotoneLinear):
    description = {'author': u'А. Куракин', 'name': u'Монотонная линейная КО'}


class MonotoneAffine(object):
    def __init__(self, x_learn, y_learn):
        _, y = convert(y_learn)
        x = np.dstack([np.ones(x_learn.shape[0:2]), x_learn])
        x, y = x - 0.5, y - 0.5
        self.weights = np.array([])

        for oper_number in range(1, x.shape[2] + 1):
            func_min = 100000
            func_argmin = 0

            for new_weight in np.arange(0, 2, 0.01):
                w = np.hstack([self.weights, new_weight])
                predicted = np.dot(x[:, :, :oper_number], w)
                predicted[predicted > 0.5] = 0.5
                predicted[predicted < -0.5] = -0.5
                func_value = get_quality(y + 0.5, predicted + 0.5)
                if func_value < func_min:
                    func_min, func_argmin = func_value, new_weight

            self.weights = np.hstack([self.weights, func_argmin])

    def __call__(self, x_val):
        print >> sys.stderr, "x size", x_val.shape
        print >> sys.stderr, "weights size", self.weights.shape
        print >> sys.stderr, "weights: ", self.weights

        x = np.dstack([np.ones(x_val.shape[0:2]), x_val])
        result = np.dot(x - 0.5, self.weights) + 0.5
        result[result > 1] = 1
        result[result < 0] = 0
        return result

    def describe(self):
        return {'weights': map(float, self.weights)}

@corrector("monotone_affine_lobacheva")
class MonotoneAffineLovacheva(MonotoneAffine):
    description = {'author': u'Е. Лобачева', 'name': u'Монотонная аффинная КО'}

@corrector("monotone_affine_lubimceva")
class MonotoneAffineLubimceva(MonotoneAffine):
    description = {'author': u'М. Любимцева', 'name': u'Монотонная аффинная КО'}

@corrector("monotone_affine_berezin")
class MonotoneAffineBerezin(MonotoneAffine):
    description = {'author': u'А. Березин', 'name': u'Монотонная аффинная КО'}

class SpecialAffine(object):
    def __init__(self, x_learn, y_learn):
        _, y = convert(y_learn)
        x = x_learn
        x, y = x - 0.5, y - 0.5
        self.weights = np.array([1])

        for oper_number in range(2, x.shape[2] + 1):
            func_min = 100000
            func_argmin = 0

            for new_weight in np.arange(-2, 2, 0.01):
                w = np.hstack([self.weights, new_weight])
                predicted = np.dot(x[:, :, :oper_number], w)
                predicted[predicted > 0.5] = 0.5
                predicted[predicted < -0.5] = -0.5
                func_value = get_quality(y + 0.5, predicted + 0.5)

                if func_value < func_min:
                    func_min, func_argmin = func_value, new_weight

            self.weights = np.hstack([self.weights, func_argmin])

    def __call__(self, x_val):
        print >> sys.stderr, "x size", x_val.shape
        print >> sys.stderr, "weights size", self.weights.shape
        print >> sys.stderr, "weights: ", self.weights

        result = np.dot(x_val - 0.5, self.weights) + 0.5
        result[result > 1] = 1
        result[result < 0] = 0
        return result

    def describe(self):
        return {'weights': map(float, self.weights)}

@corrector("special_affine_malysheva")
class SpecialAffineMalysheva(SpecialAffine):
    description = {'author': u'Е. Малышева', 'name': u'Специальная аффинная КО'}

@corrector("special_affine_morozova")
class SpecialAffineMorozova(SpecialAffine):
    description = {'author': u'Д. Морозова', 'name': u'Специальная аффинная КО'}

@corrector("special_affine_fonarev")
class SpecialAffineFonarev(SpecialAffine):
    description = {'author': u'А. Фонарев', 'name': u'Специальная аффинная КО'}

class SpecialMonotoneAffine(object):
    def __init__(self, x_learn, y_learn):
        _, y = convert(y_learn)
        x = x_learn
        x, y = x - 0.5, y - 0.5
        self.weights = np.array([1])

        for oper_number in range(2, x.shape[2] + 1):
            func_min = 100000
            func_argmin = 0

            for new_weight in np.arange(0, 2, 0.01):
                w = np.hstack([self.weights, new_weight])
                predicted = np.dot(x[:, :, :oper_number], w)
                predicted[predicted > 0.5] = 0.5
                predicted[predicted < -0.5] = -0.5
                func_value = get_quality(y + 0.5, predicted + 0.5)

                if func_value < func_min:
                    func_min, func_argmin = func_value, new_weight

            self.weights = np.hstack([self.weights, func_argmin])

    def __call__(self, x_val):
        print >> sys.stderr, "x size", x_val.shape
        print >> sys.stderr, "weights size", self.weights.shape
        print >> sys.stderr, "weights: ", self.weights

        result = np.dot(x_val - 0.5, self.weights) + 0.5
        result[result > 1] = 1
        result[result < 0] = 0
        return result

    def describe(self):
        return {'weights': map(float, self.weights)}

@corrector("special_monotone_affine_gavrikov")
class SpecialMonotoneAffineGavrikov(SpecialMonotoneAffine):
    description = {'author': u'М. Гавриков', 'name': u'Специальная монотонная аффинная КО'}

@corrector("special_monotone_affine_romov")
class SpecialMonotoneAffineRomov(SpecialMonotoneAffine):
    description = {'author': u'П. Ромов', 'name': u'Специальная монотонная аффинная КО'}

@corrector("special_monotone_affine_fonarev")
class SpecialMonotoneAffineFonarev(SpecialMonotoneAffine):
    description = {'author': u'А. Фонарев', 'name': u'Специальная монотонная аффинная КО'}

class UnstableMonotoneLinear(object):
    def __init__(self, x_learn, y_learn):
        _, y = nclass_to_nbinary(y_learn)
        #x = np.swapaxes(x_learn, 1, 2)
        w = np.random.randn(np.shape(x)[2])
        print "x size", x.shape
        print "y size", y.shape

        func = lambda w: np.sum((np.dot(x, w) - y) ** 2) \
                + 10000 * np.sum(np.float32(w < 0)) \
                + np.sum(w ** 2)

        self.weights = np.random.randn(np.shape(x)[2])
        print "weights size", self.weights.shape
        optimizer = CMAES(func, self.weights)
        optimizer.minimize = True
        self.weights = optimizer.learn()[0]

    def __call__(self, x_val):
        print "x size", x_val.shape
        print "weights size", self.weights.shape

        return np.dot(x_val, self.weights)

if __name__ == '__main__':
    x_learn = np.round(np.random.random([5, 4, 3]) * 5)
    print x_learn
    y_learn = np.array([1,2,3,4,1])
    x_test = np.round(np.random.random([5, 4, 3]) * 5)

    c = MonotoneAffine(x_learn, y_learn)
    print c.weights
    print c(x_test)
