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

KONDRASHKIN = u'Д. Кондрашкин'


class NaiveBayesian(Classifier):
    def __init__(self, x_train, y_train):
        Classifier.__init__(self, GaussianNB(), x_train, y_train)

@classifier('naive_bayesian_potapenko')
class NaiveBayesianPotapenko(NaiveBayesian):
    description = {'author': u'А. Потапенко', 'name': u'Наивный байес'}

@classifier('naive_bayesian_kondr')
class NaiveBayesianKondr(NaiveBayesian):
    description = {'author': u'Д. Кондрашкин', 'name': u'Наивный байес'}

@classifier('naive_bayesian_lobacheva')
class NaiveBayesianLobacheva(NaiveBayesian):
    description = {'author': u'Е. Лобачева', 'name': u'Наивный байес'}

@classifier('naive_bayesian_shai')
class NaiveBayesianShai(NaiveBayesian):
    description = {'author': u'И. Шаймарданов', 'name': u'Наивный байес'}

@classifier('naive_bayesian_romov')
class NaiveBayesianRomov(NaiveBayesian):
    description = {'author': u'П. Ромов', 'name': u'Наивный байес'}

@classifier('naive_bayesian_ismagilov')
class NaiveBayesianPotapenko(NaiveBayesian):
    description = {'author': u'Т. Исмагилов', 'name': u'Наивный байес'}

#@classifier('linear_standard')
class LinearStandard(Classifier):
    description = {
        'name': u'Простой линейный',
        'author': KONDRASHKIN,
    }

    def __init__(self, x_train, y_train):
        Classifier.__init__(self, LogisticRegression(fit_intercept=False), x_train, y_train)


class LinearAffine(Classifier):
    def __init__(self, x_train, y_train):
        Classifier.__init__(self, LogisticRegression(fit_intercept=True), x_train, y_train)

@classifier('linear_affine_mal')
class LinearAffineMal(NaiveBayesian):
    description = {
        'name': u'Линейный аффинный',
        'author': u'Е. Малышева',
    }

@classifier('linear_affine_mor')
class LinearAffineMor(NaiveBayesian):
    description = {
        'name': u'Линейный аффинный',
        'author': u'Д. Морозова',
    }

@classifier('linear_affine_lub')
class LinearAffineLub(NaiveBayesian):
    description = {
        'name': u'Линейный аффинный',
        'author': u'М. Любимцева',
    }

@classifier('linear_polynomial')
class LinearPolynomial(Classifier):
    description = {
        'name': u'Полиномиальный',
        'author': 'folk',
    }

    def __init__(self, x_train, y_train):
        Classifier.__init__(self, SVC(kernel='poly', probability=True), x_train, y_train)


class DecisionTree(Classifier):
    def __init__(self, x_train, y_train):
        Classifier.__init__(self, DecisionTreeClassifier(max_depth=1), x_train, y_train)

@classifier('decision_tree_fon')
class DecisionTreeFon(DecisionTree):
    description = {
        'name': u'Решающий пень',
        'author': u'А. Фонарев',
    }

@classifier('decision_tree_lob')
class DecisionTreeLob(DecisionTree):
    description = {
        'name': u'Решающий пень',
        'author': u'Е. Лобачева',
    }

@classifier('decision_tree_ber')
class DecisionTreeBer(DecisionTree):
    description = {
        'name': u'Решающий пень',
        'author': u'А. Березин',
    }


class KNN(Classifier):
    def __init__(self, x_train, y_train):
        Classifier.__init__(self, KNeighborsClassifier(n_neighbors=5, algorithm='brute'), x_train, y_train)

@classifier('KNN_nizh')
class KNNNizh(KNN):
    description = {
        'name': u'k-NN',
        'author': u'Е. Нижибицкий',
    }
@classifier('KNN_mal')
class KNNMal(KNN):
    description = {
        'name': u'k-NN',
        'author': u'Е. Малышева',
    }
@classifier('KNN_fon')
class KNNFon(KNN):
    description = {
        'name': u'k-NN',
        'author': u'А. Фонарев',
    }
@classifier('KNN_kon')
class KNNKon(KNN):
    description = {
        'name': u'k-NN',
        'author': u'Д. Кондрашкин',
    }
@classifier('KNN_nov')
class KNNNov(KNN):
    description = {
        'name': u'k-NN',
        'author': u'М. Новиков',
    }
@classifier('KNN_ogn')
class KNNOgn(KNN):
    description = {
        'name': u'k-NN',
        'author': u'Д. Огнева',
    }
