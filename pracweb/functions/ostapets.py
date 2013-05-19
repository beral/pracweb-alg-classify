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
    
    
@corrector("priority_nizhibitsky")
class PriorityNizhibitsky(MonotoneAffine):
    description = {'author': u'Е. Нижибицкий', 'name': u'Комитет старшинства'}

@corrector("priority_zak")
class PriorityZak(MonotoneAffine):
    description = {'author': u'Е. Зак', 'name': u'Комитет старшинства'}

@corrector("priority_kondrashkin")
class PriorityKondrashkin(MonotoneAffine):
    description = {'author': u'Д. Кондрашкин', 'name': u'Комитет старшинства'}
    
@corrector("priority_berezin")
class PriorityBerezin(MonotoneAffine):
    description = {'author': u'А. Березин', 'name': u'Комитет старшинства'}    
    
@corrector("priority_ogneva")
class PriorityOgneva(MonotoneAffine):
    description = {'author': u'Д. Огнева', 'name': u'Комитет старшинства'} 
    
    
@corrector("decision_list_potapenko")
class DecisionListPotapenko(SpecialAffine):
    description = {'author': u'А. Потапенко', 'name': u'Комитет большинства'}

@corrector("decision_list_fonarev")
class DecisionListFonarev(SpecialAffine):
    description = {'author': u'Е. Фонарев', 'name': u'Комитет большинства'}

@corrector("decision_list_lybimtseva")
class DecisionListLybimtseva(SpecialAffine):
    description = {'author': u'М. Любимцева', 'name': u'Комитет большинства'}
    
    @corrector("decision_list_romov")
class DecisionListRomov(SpecialAffine):
    description = {'author': u'П. Ромов', 'name': u'Комитет большинства'}

@corrector("decision_list_ostapets")
class DecisionListOstapets(SpecialAffine):
    description = {'author': u'А. Остапец', 'name': u'Комитет большинства'}

@corrector("decision_list_kurakin")
class DecisionListKurakin(SpecialAffine):
    description = {'author': u'А. Куракин', 'name': u'Комитет большинства'}

@corrector("decision_list_novikov")
class DecisionListNovikov(SpecialAffine):
    description = {'author': u'М. Новиков', 'name': u'Комитет большинства'}
    

if __name__ == '__main__':
    x_learn = np.round(np.random.random([5, 4, 3]) * 5)
    y_learn = np.array([1,2,3,4,1])
    x_test = np.round(np.random.random([15, 4, 3]) * 5)

    c = IndependentOptimumOstapets(x_learn, y_learn)
    print c.oper_number
    print c(x_test)
