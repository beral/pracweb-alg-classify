try:
    from pracweb.registry import classifier, corrector
except ImportError:
    # Dummies
    classifier = lambda x: lambda y: y
    corrector = classifier


@classifier("test")
def test_classifier():
    pass


@corrector("test")
def test_corrector():
    pass
