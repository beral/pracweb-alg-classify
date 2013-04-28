try:
    from pracweb.registry import classifier, corrector
except ImportError:
    # Dummies
    classifier = lambda x: lambda y: y
    corrector = classifier


@corrector("mean")
class Mean(object):
    def __init__(self, x_learn, y_learn, n_classes):
        pass

    def __call__(self, x_val):
        return x_val.mean(2)
