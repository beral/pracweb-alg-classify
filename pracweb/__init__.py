# encoding: utf-8

import glob
import os
import os.path
from collections import namedtuple

import flask
from flask import Flask, request, render_template

import numpy as np


Dataset = namedtuple('Dataset', ['learn', 'control', 'class_names'])


app = Flask('pracweb')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/classifier', methods=['POST'])
def classifier():
    data = request.json
    dataset = parse_request(data)
    return str(dataset)


def parse_request(data):
    objects = data['objects']
    assert isinstance(objects, list)
    n = len(objects)
    assert n > 0

    classes = set(obj['c'] for obj in objects)
    class_names = dict(enumerate(sorted(classes)))
    rev_class_names = dict((name, n) for n, name in class_names.iteritems())

    learn = []
    control = []
    for obj in objects:
        desc = (obj['x'], obj['y'], rev_class_names[obj['c']])
        if obj['t']:
            learn.append(desc)
        else:
            control.append(desc)

    n_learn = (
        np.array([(x, y) for x, y, _ in learn], dtype=float),
        np.array([c for _, _, c in learn], dtype=int),
    )
    n_control = (
        np.array([(x, y) for x, y, _ in control], dtype=float),
        np.array([c for _, _, c in control], dtype=int),
    )

    return Dataset(n_learn, n_control, class_names)
