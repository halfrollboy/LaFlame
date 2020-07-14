from __future__ import absolute_import, unicode_literals
from celery import shared_task

@shared_task
def adding_task(x, y):  
    z=x + y
    return z

@shared_task
def add(x, y):
    return x + y
