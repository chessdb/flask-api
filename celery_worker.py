import os

from celery import Celery

import config
from src import create_app
from src.tasks import *


def create_celery(flask_app):
    my_celery = Celery(
        main=flask_app.import_name,
        backend=flask_app.config["CELERY_RESULT_BACKEND"],
        broker=flask_app.config["BROKER_URL"],
        timezone=flask_app.config["CELERY_TIMEZONE"],
        include=[]
    )

    my_celery.conf.update(flask_app.config)
    task_base = my_celery.Task

    class ContextTask(task_base):
        abstract = True

        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return task_base.__call__(self, *args, **kwargs)

    my_celery.Task = ContextTask
    return my_celery


APP = create_app(os.environ['APP_CONFIG'] or config.ProductionConfig)
CELERY = create_celery(flask_app=APP)
