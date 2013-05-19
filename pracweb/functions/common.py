from sklearn.multiclass import OneVsRestClassifier


class Classifier(object):
    '''Classifier base class. Uses OneVsRest for multiclass problems'''
    def __init__(self, clf, x_train, y_train):
        n_classes = len(set(y_train))
        if n_classes > 2:
            self.clf = OneVsRestClassifier(clf)
        else:
            self.clf = clf
        self.clf.fit(x_train, y_train)

    def __call__(self, x_val):
        return self.clf.predict_proba(x_val)

    def describe(self):
        return dict(
            (k, v)
            for k, v in self.clf.get_params().iteritems()
            if not callable(v))

