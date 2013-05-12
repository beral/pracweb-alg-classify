#!/usr/bin/env python
# encoding: utf-8

import sys
from pprint import pprint
import warnings

import numpy as np
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split
from sklearn.datasets import load_iris

import pracweb.functions
import pracweb.registry as reg
import pracweb.engine as engine
import pracweb.request_parser as T


def make_iris_dataset():
    iris = load_iris()
    X, y = iris.data, iris.target
    X = X[:, [0, 2]]
    x_train, x_test, y_train, y_test = train_test_split(X, y)
    return x_train, x_test, y_train, y_test, iris.target_names


DATASETS = {
    'iris': make_iris_dataset(),
}


def print_table(table):
    col_width = [0] * len(table[0])
    for row in table:
        for i, value in enumerate(row):
            col_width[i] = max(col_width[i], len(str(value)))
    for row in table:
        print '    '.join(str(value).rjust(col_width[i])
                          for i, value in enumerate(row))


def test_single_classifiers(classifiers):
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


def test_oneshot(classifiers, corrector):
    for data_name in DATASETS:
        print '== Testing {0} x {1} vs. {2}'.format(
            sorted(classifiers),
            corrector,
            data_name
        )

        x_train, x_test, y_train, y_test, target_names = \
            DATASETS[data_name]

        problem = T.Problem(
            data=T.Dataset(
                learn=(x_train, y_train),
                test=(x_test, y_test),
                class_names=target_names
            ),
            model=T.Model(
                classifiers=classifiers,
                corrector=corrector,
            ),
            colormap=None,
            grid=None,
        )

        model = engine.solve(problem)
        metrics_data, conf_data = engine.eval_model(model, problem)
        print "=== Metrics:"
        print_table(metrics_data)
        print "=== Confusion matrix:"
        print_table(conf_data)
        print


def test_Nto1(classifiers, correctors):
    for current_corrector in correctors:
        test_oneshot(classifiers, current_corrector)


def main():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        if len(sys.argv) > 1:
            test_single_classifiers(sys.argv[1:])
        else:
            test_Nto1(reg.classifiers, reg.correctors)


if __name__ == '__main__':
    main()
