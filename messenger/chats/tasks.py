import json

from application.celery import app
from centrifugo.utils import get_statistic, publish_data
from utils.mail import send_chat_add_notification


@app.task(time_limit=60)
def publish_chat(chat, channel):
    publish_data(data=chat, channel=channel)


@app.task(time_limit=300)
def send_invitation(inviter, chat, recipients):
    send_chat_add_notification(inviter, chat, recipients)


@app.task()
def save_channels_stats():
    with open('stats.json', 'w') as file:
        json.dump(get_statistic(), file)
