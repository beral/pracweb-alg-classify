# encoding: utf-8

import glob
import os
import os.path

import flask
from flask import Flask, request, render_template

import numpy as np

import pracweb.registry as reg
import pracweb.functions
from pracweb.request_parser import parse_request


app = Flask('pracweb')


@app.route('/')
def index():
    return render_template(
        'index.html',
        classifiers=reg.classifiers,
        correctors=reg.correctors)


@app.route('/classifier', methods=['POST'])
def classifier():
    try:
        problem = parse_request(request.json)
        return "ok"
    except ValueError as e:
        print e.message
        return (e.message, 400, ())
    except Exception as e:
        return ('unknown error %s' % e.__class__.__name__, 500, ())
