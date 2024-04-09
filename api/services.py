from typing import List

import requests
from requests import Response
from telebot.types import Message

from api.conf import REQUEST_DETAILS
from api.decorators.request import request
from core.conf import bot
from core.globals import *


def get_auth_headers() -> dict:
    return {"Authorization": f"Bearer {REQUEST_DETAILS[ACCESS_TOKEN_KEY]}"}


@request(url=URL_BOT_USER_VALUE)
def get_or_create_user(message: Message, url: str) -> Response | dict:
    user_id = str(message.from_user.id)

    data = {
        USER_ID_KEY: user_id,
        BOT_ID_KEY: REQUEST_DETAILS[BOT_ID_KEY],
        ADDITIONAL_KEY: message.from_user.to_json()
    }

    response = requests.post(url, json=data, headers=get_auth_headers())

    return response


@request(url=URL_BOT_USER_VALUE)
def update_user(message: Message, url: str) -> Response | dict:
    user_id = str(message.from_user.id)

    data = {
        USER_ID_KEY: user_id,
        BOT_ID_KEY: REQUEST_DETAILS[BOT_ID_KEY],
        ADDITIONAL_KEY: message.from_user.to_json(),
        OCCUPATION_TITLE_KEY: USERS_TMP[user_id].get(OCCUPATION_TITLE_KEY, None),
        STATUS_TITLE_KEY: USERS_TMP[user_id].get(STATUS_TITLE_KEY, None),
        IS_FINISHED_KEY: USERS_TMP[user_id].get(IS_FINISHED_KEY, None),
        LANGUAGE_KEY: USERS_TMP[user_id].get(LANGUAGE_KEY, None),
        STATUS_ID_KEY: USERS_TMP[user_id].get(STATUS_ID_KEY, None),
    }

    response = requests.patch(url, json=data, headers=get_auth_headers())

    return response


@request(url=URL_STATUSES_BY_BOT_VALUE)
def get_all_statuses_by_bot(url: str) -> Response | List[dict]:
    bot_id = REQUEST_DETAILS[BOT_ID_KEY]
    url = url.format(bot_id)

    response = requests.get(url, headers=get_auth_headers())
    return response


@request(url=URL_OCCUPATIONS_BY_BOT_VALUE)
def get_all_occupations_by_status(user_id: str, url: str) -> Response | List[dict]:
    status_id = USERS_TMP[user_id][STATUS_ID_KEY]
    url = url.format(status_id)

    response = requests.get(url, headers=get_auth_headers())
    return response


@request(url=URL_STATIC_TEMPLATE_BY_BOT_VALUE)
def get_all_static_templates_by_bot(url: str) -> Response | List[dict]:
    bot_id = REQUEST_DETAILS[BOT_ID_KEY]
    url = url.format(bot_id)

    response = requests.get(url, headers=get_auth_headers())
    return response


@request(url=URL_ANIMATED_TEMPLATE_BY_BOT_VALUE)
def get_all_animated_templates_by_bot(url: str) -> Response | List[dict]:
    bot_id = REQUEST_DETAILS[BOT_ID_KEY]
    url = url.format(bot_id)

    response = requests.get(url, headers=get_auth_headers())
    return response


@request(url=URL_TEMPLATE_BY_ID_VALUE)
def get_template_by_id(template_id: str | int, url: str) -> Response | dict:
    url = url.format(template_id)

    response = requests.get(url, headers=get_auth_headers())
    return response


@request(url=URL_REQUEST_VALUE)
def create_request(data: dict, url: str) -> Response | dict:
    request_data = {
        USER_ID_KEY: data[TELEGRAM_ID_KEY],
        TEMPLATE_ID_KEY: data[TEMPLATE_KEY][ID_KEY],
        USER_OVERLAY_CHOICE_KEY: data[USER_OVERLAY_CHOICE_KEY],
        OCCUPATION_ID_KEY: data[OCCUPATION_KEY][ID_KEY],
        BOT_ID_KEY: str(bot.get_me().id)
    }

    response = requests.post(url, json=request_data, headers=get_auth_headers())
    return response
