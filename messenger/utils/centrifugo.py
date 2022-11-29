import json

import jwt
import requests
from django.core.serializers.json import DjangoJSONEncoder

from application.config import (CENTRIFUGO_API_KEY,
                                CENTRIFUGO_TOKEN_HMAC_SECRET_KEY,
                                CENTRUFUGO_API_URL)


def generate_connection_token(user_id):
    return jwt.encode({'sub': f'{user_id}'}, CENTRIFUGO_TOKEN_HMAC_SECRET_KEY, algorithm="HS256")


def generate_subscription_token(client, channel):
    return jwt.encode({'sub': f'{client}', 'channel': f'{channel}'}, CENTRIFUGO_TOKEN_HMAC_SECRET_KEY, algorithm="HS256")


def publish_data(data, channel):
    command = {
        'method': 'publish',
        'params': {
            'channel': f'{channel}',
            'data': data
        }
    }
    json_data = json.dumps(command, cls=DjangoJSONEncoder)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'apikey ' + CENTRIFUGO_API_KEY
    }
    requests.post(CENTRUFUGO_API_URL, data=json_data, headers=headers)


def get_statistic():
    command = {
        "method": "channels",
        "params": {}
    }
    json_data = json.dumps(command)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'apikey ' + CENTRIFUGO_API_KEY
    }
    response = requests.post(CENTRUFUGO_API_URL,
                             data=json_data, headers=headers)
    return json.loads(response.text)['result']
