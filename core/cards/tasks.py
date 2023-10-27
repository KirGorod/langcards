from core.celery import app as celery_app
from celery import shared_task


@celery_app.task(name='cards.tasks.add_numbers')
# @shared_task
def add_numbers(a, b):
    res = a + b
    print(res)
    return res
