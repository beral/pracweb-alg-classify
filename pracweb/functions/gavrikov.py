# vim: et sw=4
# encoding: utf-8

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


NEURALNET_HIDDEN_DIM = 5


def nclass_to_nbinary(y):
    dim = len(set(y))
    flags = np.zeros((y.size, dim))
    for i, c in enumerate(y):
        flags[i, c] = 1
    return dim, flags


#@classifier("neuralnet")
class NeuralNet(object):
    def __init__(self, x_train, y_train):
        dim, y_train2 = nclass_to_nbinary(y_train)
        ds = SupervisedDataSet(2, dim)
        for (x, y) in zip(x_train, y_train2):
            ds.addSample(x, y)

        # change 5 to any value change the count of hidden nodes
        self.dim = dim
        self.net = buildNetwork(2, NEURALNET_HIDDEN_DIM, dim,
                                hiddenclass=TanhLayer)
        trainer = BackpropTrainer(self.net, ds)
        trainer.train()

    def __call__(self, x):
        result = np.empty((x.shape[0], self.dim))
        net = self.net
        for i in xrange(0, x.shape[0]):
            result[i, :] = net.activate(x[i, :])
        return result


#@corrector("polynomial")
def corrector_polynomial(x_train, y_train, n_classes):
    clf = SVC(kernel='poly', degree=2, probability=True)
    clf = OneVsRestClassifier(clf)
    clf.fit(x_train, y_train)
    return clf.predict_proba  # FIXME: dimensions?


#@corrector("monotone_special")
def corrector_monotone_special(x_train, y_train, n_classes):
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
    return lambda xx: np.dot(w_opt, x)  # FIXME: dimensions?


def test_iris():
    from sklearn.cross_validation import train_test_split
    from sklearn.datasets import load_iris
    iris = load_iris()
    X, y = iris.data, iris.target
    X = X[:, [0, 2]]
    x_train, x_test, y_train, y_test = train_test_split(X, y)
    return x_train, x_test, y_train, y_test


def run_test():
    import pylab as pl
    x_train, x_test, y_train, y_test = test_iris()
    func = NeuralNet(x_train, y_train)
    y_pred = np.argmax(func(x_test))

    pl.scatter(x_test[:, 0], x_test[:, 1],
               c=y_pred, alpha=0.3, s=100, marker='s')
    pl.scatter(x_test[:, 0], x_test[:, 1],
               c=y_test, alpha=0.7, s=50)
    pl.show()

if __name__ == '__main__':
    run_test()