import json

from application.celery import app
from centrifugo.utils import get_statistic


@app.task(time_limit=60)
def save_channels_stats():
    with open('stats.json', 'w') as file:
        json.dump(get_statistic(), file, indent=4)
