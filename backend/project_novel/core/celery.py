import os
from celery import Celery

# manage.py 와 같은 경로에 위치한 settings.py 모듈을 임포트
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")


# task 지정 decorator
@app.task
def add_numbers():
    return 

# inform celery to look for tasks.py in each app
app.autodiscover_tasks()