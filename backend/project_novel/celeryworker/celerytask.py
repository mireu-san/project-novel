from celery import Celery


app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')
app.config_from_object('celeryconfig')

@app.task
def add_numbers():
    return