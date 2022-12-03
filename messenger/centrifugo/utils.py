import json
import time

import jwt
import requests
from django.core.serializers.json import DjangoJSONEncoder

from application.config import (CENTRIFUGO_API_KEY,
                                CENTRIFUGO_CONNECT_TOKEN_EXPIRE,
                                CENTRIFUGO_SUBSCRIBE_TOKEN_EXPIRE,
                                CENTRIFUGO_TOKEN_HMAC_SECRET_KEY,
                                CENTRUFUGO_API_URL)


def generate_connection_token(user_id):
    claims = {'sub': f'{user_id}', 'exp': int(
        time.time()) + CENTRIFUGO_CONNECT_TOKEN_EXPIRE}
    return jwt.encode(claims, CENTRIFUGO_TOKEN_HMAC_SECRET_KEY, algorithm="HS256")


def generate_subscription_token(client, channel):
    claims = {'sub': f'{client}', 'channel': f'{channel}', 'exp': int(
        time.time()) + CENTRIFUGO_SUBSCRIBE_TOKEN_EXPIRE}
    return jwt.encode(claims, CENTRIFUGO_TOKEN_HMAC_SECRET_KEY, algorithm="HS256")


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
