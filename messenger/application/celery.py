import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')


app = Celery('application')

app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.timezone = 'Europe/Moscow'

app.conf.beat_schedule = {
    'gen-channels-stats-every-30-secs': {
        'task': 'chats.tasks.save_channels_stats',
        'schedule': 30
    }
}
