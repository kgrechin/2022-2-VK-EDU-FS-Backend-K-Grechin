import os

from celery import Celery

from utils.env import getenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

app = Celery('application')

app.conf.broker_url = getenv('CELERY_BROKER_URL')
app.conf.result_backend = getenv('CELERY_BROKER_BACKEND')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.timezone = 'Europe/Moscow'

app.conf.beat_schedule = {
    'gen-channels-stats-every-30-secs': {
        'task': 'centrifugo.tasks.save_channels_stats',
        'schedule': 30
    }
}
