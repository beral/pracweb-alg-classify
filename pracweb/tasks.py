from celery import Celery, current_task

import pracweb.flags as flags
if not flags.IS_CLIENT:
    from . import functions
    from .registry import classifiers, correctors
    from .request_parser import parse_request
    from .engine import solve, build_map, make_visuals, store_images


celery = Celery("engine",
                broker='redis://localhost:6379/0',
                backend='redis')


@celery.task
def get_functions():
    return classifiers.keys(), correctors.keys()


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
    report_progress(5, "Building model...")
    model = solve(problem)
    report_progress(30, "Evaluating model...")
    estimate_map = build_map(model, problem)
    report_progress(70, "Drawing maps...")
    visuals = make_visuals(estimate_map, problem)
    report_progress(95, "Saving maps...")
    image_paths = store_images(visuals, task_id, config['store_path'])
    report_progress(100, "Done")
    return True, {
        'result_id': task_id,
        'maps': image_paths,
    }