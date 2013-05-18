# -*- coding: utf-8 -*-

from celery import Celery, current_task

import pracweb.flags as flags
if not flags.IS_CLIENT:
    from datetime import datetime
    from collections import Iterable
    import operator
    import os.path
    import Image
    import json
    from . import functions
    from .registry import classifiers, correctors
    from .request_parser import parse_request
    from .engine import solve, describe_model, eval_model, build_map, make_visuals


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
                'progress': int(progress),
                'comment': comment
            })

    def deep_map(f, x):
        if isinstance(x, Iterable):
            return reduce(operator.add, (deep_map(f, y) for y in x))
        else:
            return [f(x)]

    task_id = current_task.request.id

    report_progress(0, "Validating...")
    try:
        problem = parse_request(request)
    except ValueError as e:
        # Validation error
        return False, str(e)

    task_dir = os.path.join(config['store_path'], task_id)
    os.mkdir(task_dir)
    with open(os.path.join(task_dir, 'request.json'), 'w') as f:
        json.dump(request, f)

    meta = {
        'start_time': datetime.now().isoformat(),
    }
    with open(os.path.join(task_dir, 'meta.json'), 'w') as f:
        json.dump(meta, f)

    report_progress(5, "Learning")
    model = solve(problem)

    results = []
    submodels = model[0] + [model]
    progress = 30.0
    progress_delta = (100 - progress) / len(submodels)

    for index, submodel in enumerate(submodels):
        description = describe_model(submodel)
        if len(problem.data.test[0]):
            report_progress(progress, "Testing")
            metrics_data, conf_data = eval_model(submodel, problem)
        else:
            metrics_data = None
            conf_data = None
        progress += 0.2 * progress_delta

        report_progress(progress, "Building maps")
        estimate_map = build_map(submodel, problem)
        progress += 0.6 * progress_delta

        report_progress(progress, "Drawing maps")
        visuals = make_visuals(estimate_map, problem)
        progress += 0.1 * progress_delta

        report_progress(progress, "Saving maps")
        image_paths = store_images(visuals, task_id, index, task_dir)
        progress += 0.1 * progress_delta

        report_progress(progress, "Done")
        results.append({
            'model': deep_map(operator.attrgetter('__prac__'), submodel),
            'maps': image_paths,
            'metrics': metrics_data,
            'confusion_matrix': conf_data,
            'text': description,
        })
    response = {
        'result_id': task_id,
        'results': results
    }
    with open(os.path.join(task_dir, 'response.json'), 'w') as f:
        json.dump(response, f)

    return True, response


def store_images(images, task_id, group_id, store_path):
    '''Сохранить картинки диаграмм на диск'''

    paths = dict()
    for name, imgbuf in images.iteritems():
        Image.fromarray(imgbuf).save(os.path.join(
            store_path,
            '{0}_{1}.png'.format(group_id, name)))
        paths[name] = 'result/{0}/{1}_{2}.png'.format(task_id, group_id, name)
    return paths
