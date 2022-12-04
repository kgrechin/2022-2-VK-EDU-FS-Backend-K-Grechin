import json
import time

import jwt
import requests
from django.core.serializers.json import DjangoJSONEncoder

from utils.env import getenv

API_URL = getenv('CENTRUFUGO_API_URL')
API_KEY = getenv('CENTRIFUGO_API_KEY')
TOKEN_HMAC_SECRET_KEY = getenv('CENTRIFUGO_TOKEN_HMAC_SECRET_KEY')
CONNECT_TOKEN_EXPIRE = int(getenv('CENTRIFUGO_CONNECT_TOKEN_EXPIRE'))
SUBSCRIBE_TOKEN_EXPIRE = int(getenv('CENTRIFUGO_SUBSCRIBE_TOKEN_EXPIRE'))


def generate_connection_token(user_id):
    claims = {'sub': f'{user_id}', 'exp': int(
        time.time()) + CONNECT_TOKEN_EXPIRE}
    return jwt.encode(claims, TOKEN_HMAC_SECRET_KEY, algorithm="HS256")


def generate_subscription_token(client, channel):
    claims = {'sub': f'{client}', 'channel': f'{channel}', 'exp': int(
        time.time()) + SUBSCRIBE_TOKEN_EXPIRE}
    return jwt.encode(claims, TOKEN_HMAC_SECRET_KEY, algorithm="HS256")


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
        'Authorization': 'apikey ' + API_KEY
    }
    requests.post(API_URL, data=json_data, headers=headers)


def get_statistic():
    command = {
        "method": "channels",
        "params": {}
    }
    json_data = json.dumps(command)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'apikey ' + API_KEY
    }
    response = requests.post(API_URL, data=json_data, headers=headers)
    return json.loads(response.text)['result']
