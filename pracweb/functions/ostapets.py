# -*- coding: utf-8 -*-

import numpy as np
import sys

try:
    from pracweb.registry import classifier, corrector
except ImportError:
    # Dummies
    classifier = lambda x: lambda y: y
    corrector = classifier

class IndependentOptimum(object):
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

        return np.array(x_val[:,:,self.oper_number])

    def describe(self):
        return {'algo number': self.oper_number}
    
@corrector("independent_optimum_ostapets")
class IndependentOptimumOstapets(IndependentOptimum):
    description = {'author': u'А. Остапец', 'name': u'Выбирающая независимый оптимум КО'}

@corrector("independent_optimum_nizhibitsky")
class IndependentOptimumNizhibitsky(IndependentOptimum):
    description = {'author': u'Е. Нижибицкий', 'name': u'Выбирающая независимый оптимум КО'}

@corrector("independent_optimum_berezin")
class IndependentOptimumBerezin(IndependentOptimum):
    description = {'author': u'А. Березин', 'name': u'Выбирающая независимый оптимум КО'}

@corrector("independent_optimum_ogneva")
class IndependentOptimumOgneva(IndependentOptimum):
    description = {'author': u'Д. Огнева', 'name': u'Выбирающая независимый оптимум КО'}

if __name__ == '__main__':
    x_learn = np.round(np.random.random([5, 4, 3]) * 5)
    y_learn = np.array([1,2,3,4,1])
    x_test = np.round(np.random.random([15, 4, 3]) * 5)

    c = IndependentOptimumOstapets(x_learn, y_learn)
    print c.oper_number
    print c(x_test)
