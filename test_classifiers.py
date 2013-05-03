#!/usr/bin/env python
# encoding: utf-8

import sys
import numpy as np
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split
from sklearn.datasets import load_iris

import pracweb.functions
import pracweb.registry as reg


def make_iris_dataset():
    iris = load_iris()
    X, y = iris.data, iris.target
    X = X[:, [0, 2]]
    x_train, x_test, y_train, y_test = train_test_split(X, y)
    return x_train, x_test, y_train, y_test, iris.target_names


DATASETS = {
    'iris': make_iris_dataset(),
}


def main():

    if len(sys.argv) > 1:
        classifiers = sys.argv[1:]
    else:
        classifiers = reg.classifiers.keys()

    for name in classifiers:
        for data_name in DATASETS:
            x_train, x_test, y_train, y_test, target_names = \
                DATASETS[data_name]

            classifier = reg.classifiers[name](x_train, y_train)
            y_estimates = classifier(x_test)
            y_pred = np.argmax(y_estimates, 1)
            print "=== {0} vs. {1}".format(name, data_name)
            print classification_report(y_test, y_pred,
                                        target_names=target_names)


if __name__ == '__main__':
    main()
