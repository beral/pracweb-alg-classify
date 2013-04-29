# encoding: utf-8

import glob
import os
import os.path
import traceback
import hashlib
from datetime import datetime

import flask
from flask import Flask, request, render_template, jsonify

import pracweb.registry as reg
import pracweb.functions
from pracweb.request_parser import parse_request
from pracweb.engine import process_problem


STORE_PATH = '/tmp/pracweb'

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
        app.logger.info("A: %s, C: %s",
                        problem.model.classifiers,
                        problem.model.corrector)
        reqid = "{0}_{1}".format(
            datetime.utcnow().strftime("%s"),
            hashlib.sha1(request.data).hexdigest())
        reply = process_problem(problem)
        visuals = reply['visuals']
        store_images(visuals, reqid)
        for name in visuals:
            visuals[name] = 'result/{0}_{1}.png'.format(reqid, name)

        return jsonify(reply)
    except ValueError as e:
        traceback.print_exc()
        return (str(e), 400, ())
    except Exception as e:
        traceback.print_exc()
        return (traceback.format_exc(), 500, ())


@app.route('/result/<filename>')
def result(filename):
    return flask.send_from_directory(STORE_PATH, filename)


def store_images(images, reqid):
    if not os.path.isdir(STORE_PATH):
        os.mkdir(STORE_PATH)
    for name, image in images.iteritems():
        image.save(os.path.join(
            STORE_PATH,
            '{0}_{1}.png'.format(reqid, name)))
