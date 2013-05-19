# vim: et sw=4
# -*- coding: utf-8 -*-

# nnet - neural Networks
# polynomial -- KO
# specialMonoton -- linear KO with constraints, QP with constraints
# all works
# all these funks return lambda expression
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure.modules import TanhLayer
import numpy as np

from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier

try:
    from pracweb.registry import classifier, corrector
except ImportError:
    classifier = lambda x: lambda y: y
    corrector = classifier


NEURALNET_HIDDEN_DIM = 2


def nclass_to_nbinary(y):
    dim = len(set(y))
    flags = np.zeros((y.size, dim))
    for i, c in enumerate(y):
        flags[i, c] = 2
    return dim, flags

class NeuralNet(object):
    def __init__(self, x_train, y_train):
        dim, y_train2 = nclass_to_nbinary(y_train)
        ds = SupervisedDataSet(2, dim)
        # feint ears
        for repeatCount in xrange(0, 2):
            for (x, y) in zip(x_train, y_train2):
                ds.addSample(x, y)
        self.dim = dim
        self.net = buildNetwork(2, NEURALNET_HIDDEN_DIM, dim,
                                hiddenclass=TanhLayer)
        trainer = BackpropTrainer(self.net, ds)
        trainer.trainUntilConvergence(validationProportion=0.1, maxEpochs=1000)

    def __call__(self, x):
        result = np.empty((x.shape[0], self.dim))
        net = self.net
        for i in xrange(0, x.shape[0]):
            result[i, :] = net.activate(x[i, :])
        return result

@classifier("neuralnet_lubimtceva")
class NeuralnetLubimtceva(NeuralNet):
    description = {'author': u'М. Любимцева', 'name': u'Нейронная сеть'}

@classifier("neuralnet_gavrikov")
class NeuralnetGavrikov(NeuralNet):
    description = {'author': u'М. Гавриков', 'name': u'Нейронная сеть'}

#@corrector("polynomial")
def corrector_polynomial(x_train, y_train):
    clf = SVC(kernel='poly', degree=2, probability=True)
    clf = OneVsRestClassifier(clf)
    clf.fit(x_train, y_train)
    return clf.predict_proba  # FIXME: dimensions?


#@corrector("monotone_special")
def corrector_monotone_special(x_train, y_train):
    from pybrain.optimization import CMAES
    dim, y_train2 = nclass_to_nbinary(y_train)
    y_train2 = np.array(y_train2)

    def trainOne(index):
        def opt_func(w):
            return (np.sum((np.dot(x_train, w)
                            - y_train2[:, index]) ** 2)
                    - 1000 * np.sum(np.sign(w) - 1))
        l = CMAES(opt_func, np.random.randn(np.shape(x_train)[1]))
        l.minimize = True
        opt_w = l.learn()[0]
        return opt_w

    w_opt = np.array(map(trainOne, range(dim)))
    return lambda xx: np.dot(xx, w_opt.T)
