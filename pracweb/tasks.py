# -*- coding: utf-8 -*-

from celery import Celery, current_task

import pracweb.flags as flags
if not flags.IS_CLIENT:
    from . import functions
    from .registry import classifiers, correctors
    from .request_parser import parse_request
    from .engine import solve, describe_model, eval_model, build_map, make_visuals, store_images


celery = Celery("engine",
                broker='redis://localhost:6379/0',
                backend='redis')


@celery.task
def get_functions():
    def description(x, name):
        if hasattr(x, 'description'):
            return x.description
        else:
            return {'name': name, 'author': ''}

    def describe(table):
        return dict((name, description(table[name], name))
                    for name in table)

    return describe(classifiers), describe(correctors)


@celery.task
def process_request(request, config):
    def report_progress(progress, comment):
        current_task.update_state(
            state='PROGRESS',
            meta={
                'state': 'RUNNING',
                'progress': progress,
                'comment': comment
            })

    task_id = current_task.request.id

    report_progress(0, "Validating...")
    try:
        problem = parse_request(request)
    except ValueError as e:
        # Validation error
        return False, str(e)
    report_progress(5, "Learning")
    model = solve(problem)
    description = describe_model(model)
    if len(problem.data.test[0]):
        report_progress(15, "Testing")
        metrics_data, conf_data = eval_model(model, problem)
    else:
        metrics_data = None
        conf_data = None
    report_progress(30, "Building maps")
    estimate_map = build_map(model, problem)
    report_progress(70, "Drawing maps")
    visuals = make_visuals(estimate_map, problem)
    report_progress(95, "Saving maps")
    image_paths = store_images(visuals, task_id, config['store_path'])
    report_progress(100, "Done")
    return True, {
        'result_id': task_id,
        'maps': image_paths,
        'metrics': metrics_data,
        'confusion_matrix': conf_data,
        'text': description,
    }
