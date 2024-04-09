import os

import requests

from core.conf import bot
from core.globals import *


def get_tokens() -> dict:
    data = {
        EMAIL_KEY: os.getenv(ENV_LOGIN_KEY),
        PASSWORD_KEY: os.getenv(ENV_PASSWORD_KEY),
        BOT_ID_KEY: str(bot.get_me().id)
    }
    url = os.getenv(ENV_API_URL_KEY) + URL_LOGIN_VALUE
    response = requests.post(url, data)

    if response.status_code != 201:
        raise ValueError(ERROR_NOT_AUTH_KEY_TEXT)

    print("Bot authenticated and started")

    return response.json()


REQUEST_DETAILS = get_tokens()


def refresh_tokens() -> None:
    data = {
        REFRESH_TOKEN_KEY: REQUEST_DETAILS[REFRESH_TOKEN_KEY]
    }
    url = os.getenv(ENV_API_URL_KEY) + URL_ACCESS_TOKEN_VALUE
    response = requests.post(url, data)

    if response.status_code != 201:
        raise ValueError(ERROR_NOT_AUTH_KEY_TEXT)

    REQUEST_DETAILS.update(response.json())
