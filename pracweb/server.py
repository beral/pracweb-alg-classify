# encoding: utf-8

import traceback
import pprint
import os.path

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
    return flask.render_template('index.html')


@app.route('/reports/')
def reports_index():
    return flask.render_template('reports.html')


@app.route('/reports/<report_name>/')
@app.route('/reports/<report_name>/<filename>')
def report(report_name, filename='index.html'):
    templates = os.path.join(app.root_path, app.template_folder)
    rel_path = reduce(flask.safe_join, ('reports', report_name, filename))
    full_path = os.path.join(templates, rel_path)
    if not os.path.exists(full_path):
        flask.abort(404)

    if filename.endswith('.html'):
        return flask.render_template(rel_path)
    else:
        return flask.send_file(full_path)



@app.route('/api/operations')
def operations():
    classifiers, correctors = tasks.get_functions.delay().get(timeout=1)
    return flask.jsonify({
        'available': {
            'classifiers': classifiers,
            'correctors': correctors,
        },
        'default': {
            'classifiers': ['naive_bayesian'],
            'correctors': ['monotone_affine_berezin'],
        },
    })


@app.route('/api/classifier', methods=['POST'])
def classifier():
    task = tasks.process_request.delay(
        request.json,
        {'store_path': STORE_PATH})
    return flask.redirect(
        flask.url_for('check_status', task_id=task.id))


@app.route('/api/status/<task_id>')
def check_status(task_id):
    task = AsyncResult(task_id, app=tasks.celery)
    if task.ready():
        if task.successful():  # Task finished successfully
            status, result_value = task.result
            if status:  # Valid result
                app.logger.info("result: %s", pprint.pformat(result_value))
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
        response.status_code = 202
        return response


@app.route('/result/<task_id>/<filename>')
def result(task_id, filename):
    return flask.send_from_directory(
        STORE_PATH,
        '{0}_{1}'.format(task_id, filename))
