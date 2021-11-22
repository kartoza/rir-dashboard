from core.celery import app
from celery.utils.log import get_task_logger
from django.core.management import call_command

logger = get_task_logger(__name__)


@app.task
def run_harvesters():
    call_command('run_harvesters')


@app.task
def run_harvester(id):
    call_command('run_harvesters', '--id', id)
