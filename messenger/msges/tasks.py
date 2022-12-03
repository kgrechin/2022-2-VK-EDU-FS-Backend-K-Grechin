from application.celery import app
from centrifugo.utils import publish_data


@app.task(time_limit=30)
def publish_message(message, channel):
    publish_data(data=message, channel=channel)
