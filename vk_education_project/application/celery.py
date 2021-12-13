import os
from celery import Celery
from django.apps import apps


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

app = Celery('application')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
app.conf.beat_schedule = {}