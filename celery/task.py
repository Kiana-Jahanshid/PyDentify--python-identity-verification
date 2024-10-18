from celery import Celery

celeryApp = Celery("tasks" , broker="redis://redis:6379/0")

@celeryApp.task
def add_numbers(a,b):
    return a+b