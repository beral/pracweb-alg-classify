# encoding: utf-8

import os
import os.path
import traceback

import flask
from flask import Flask, request
from celery.result import AsyncResult

from . import flags
flags.IS_CLIENT = True
from . import tasks

STORE_PATH = '/tmp/pracweb'

app = Flask('pracweb')


@app.route('/')
def index():
    classifiers, correctors = tasks.get_functions.delay().get()
    return flask.render_template(
        'index.html',
        classifiers=classifiers,
        correctors=correctors)


@app.route('/classifier', methods=['POST'])
def classifier():
    task = tasks.process_request.delay(
        request.json,
        {'store_path': STORE_PATH})
    return flask.redirect(
        flask.url_for('check_status', task_id=task.id))


@app.route('/status/<task_id>')
def check_status(task_id):
    task = AsyncResult(task_id, app=tasks.celery)
    if task.ready():
        if task.successful():  # Task finished successfully
            status, result_value = task.result
            if status:  # Valid result
                return flask.jsonify(result_value)
            else:  # Handled exception
                response = flask.make_response(result_value, 400)
                response.mimetype = 'text/plain'
                return response
        else:  # Unhandled exception
            exc = task.result
            response = flask.make_response(
                traceback.format_exception_only(type(exc), exc),
                500)
            response.mimetype = 'text/plain'
            return response
    else:  # if task.ready()
        status = {
            'result_id': task.id,
            'state': 'PENDING',
            'progress': 0,
        }
        if task.state == 'PROGRESS':
            status.update(task.result)
        response = flask.jsonify(status)
        response.status_code = 206
        return response


@app.route('/result/<task_id>/<filename>')
def result(task_id, filename):
    return flask.send_from_directory(
        STORE_PATH,
        '{0}_{1}'.format(task_id, filename))
