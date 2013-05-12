# -*- coding: utf-8 -*-

import numpy as np
#from pybrain.optimization import CMAES
import sys

try:
    from pracweb.registry import classifier, corrector
except ImportError:
    # Dummies
    classifier = lambda x: lambda y: y
    corrector = classifier
    
@corrector("independent_optimum")
class IndependentOptimum(object):
    description = {'author': u'А. Остапец', 'name': u'Выбирающая независимый оптимум КО'}
    def __init__(self, x_learn, y_learn):
        x = x_learn
        votes = np.zeros(len(x))

        for i in range(len(x)):
            res = np.mean(x[i,:,:],axis=0)/np.max(x[i,:,:],axis=0)
            votes[np.argmin(res)]+=1

        self.oper_number = np.argmax(votes)

    def __call__(self, x_val):
        print >> sys.stderr, "x size", x_val.shape
        print >> sys.stderr, "algo number", self.oper_number+1

        result = x_val[:,:,self.oper_number]
        return result

    def describe(self):
        return {'algo number': self.oper_number}

if __name__ == '__main__':
    x_learn = np.round(np.random.random([5, 4, 3]) * 5)
    y_learn = np.array([1,2,3,4,1])
    x_test = np.round(np.random.random([15, 4, 3]) * 5)

    c = IndependentOptimum(x_learn, y_learn)
    print c.oper_number
    print c(x_test)
