import os
from typing import Callable

from telebot.types import Message

from api.decorators.handler_error_catcher import handler_error_catcher
from api.services import update_user, get_all_statuses_by_bot, get_all_occupations_by_status
from core.conf import bot
from core.globals import *
from core.utils import get_message_text, get_status_or_occupation_title_list
from menu.keyboards import get_menu_keyboard, get_language_keyboard, get_profile_keyboard
from menu.messages import SELECT_LANGUAGE_MESSAGE
from profile.keyboards import get_status_occupation_keyboard
from profile.messages import STATUS_MESSAGE, OCCUPATION_MESSAGE, PROFILE_FILLED_MESSAGE
from profile.utils import get_profile_message


@handler_error_catcher()
def language_handler(message: Message, telegramId: str, language: str, **kwargs) -> None:
    if message.text not in LANGUAGE_IN_RUSSIAN.keys():
        language_mode = os.getenv(ENV_LANGUAGE_MODE_KEY)
        message_text = get_message_text(SELECT_LANGUAGE_MESSAGE, language or language_mode)
        keyboard = get_language_keyboard()

        msg = bot.send_message(telegramId, message_text, reply_markup=keyboard)
        return bot.register_next_step_handler(msg, language_handler)

    USERS_TMP[telegramId][LANGUAGE_KEY] = LANGUAGE_IN_RUSSIAN[message.text]

    user = update_user(message)

    status_display(message, telegramId, user[LANGUAGE_KEY])


def status_display(message: Message, telegramId: str, language: str) -> None:
    statuses = get_all_statuses_by_bot()
    statuses_titles = get_status_or_occupation_title_list(statuses, language)

    if len(statuses_titles) > 1:
        return multiple_status_occupation_handler(STATUS_LIST_KEY, statuses_titles, telegramId, language,
                                                  STATUS_MESSAGE,
                                                  status_handler)

    USERS_TMP[telegramId][STATUS_TITLE_KEY] = statuses_titles[0]

    user = update_user(message)
    USERS_TMP[telegramId][STATUS_ID_KEY] = user[STATUS_KEY][ID_KEY]
    occupation_display(message, telegramId, user[LANGUAGE_KEY])


@handler_error_catcher()
def status_handler(message: Message, telegramId: str, language: str, **kwargs) -> None:
    status_list = USERS_TMP[telegramId][STATUS_LIST_KEY]

    if message.text not in status_list:
        return status_display(message, telegramId, language)

    USERS_TMP[telegramId][STATUS_TITLE_KEY] = message.text
    user = update_user(message)

    USERS_TMP[telegramId][STATUS_ID_KEY] = user[STATUS_KEY][ID_KEY]

    occupation_display(message, telegramId, user[LANGUAGE_KEY])


def occupation_display(message: Message, telegramId: str, language: str) -> None:
    occupations = get_all_occupations_by_status(telegramId)
    occupations_titles = get_status_or_occupation_title_list(occupations, language)

    if len(occupations_titles) > 1:
        return multiple_status_occupation_handler(OCCUPATION_LIST_KEY, occupations_titles, telegramId, language,
                                                  OCCUPATION_MESSAGE, occupation_handler)

    USERS_TMP[telegramId][OCCUPATION_TITLE_KEY] = occupations_titles[0]
    USERS_TMP[telegramId][IS_FINISHED_KEY] = True
    user = update_user(message)

    display_profile_filled(telegramId, user[LANGUAGE_KEY])


def display_profile_filled(telegramId: str, language: str) -> None:
    message_text = PROFILE_FILLED_MESSAGE[language]
    keyboard = get_menu_keyboard(language)

    bot.send_message(telegramId, message_text, reply_markup=keyboard)


def multiple_status_occupation_handler(storage_key: str, items_list: list, telegramId: str, language: str,
                                       message: dict, next_step_handler: Callable) -> None:
    USERS_TMP[telegramId][storage_key] = items_list
    keyboard = get_status_occupation_keyboard(items_list)
    message_text = message[language]

    msg = bot.send_message(telegramId, message_text, reply_markup=keyboard)
    return bot.register_next_step_handler(msg, next_step_handler)


@handler_error_catcher()
def occupation_handler(message: Message, telegramId: str, language: str, **kwargs) -> None:
    occupation_list = USERS_TMP[telegramId][OCCUPATION_LIST_KEY]

    if message.text not in occupation_list:
        return occupation_display(message, telegramId, language)

    USERS_TMP[telegramId][OCCUPATION_TITLE_KEY] = message.text
    USERS_TMP[telegramId][IS_FINISHED_KEY] = True

    user = update_user(message)

    display_profile_filled(telegramId, user[LANGUAGE_KEY])


@handler_error_catcher()
def show_profile_handler(message: Message, telegramId: str, language: str, status: dict, occupation: dict,
                         **kwargs) -> None:
    message_text = get_profile_message(language, status, occupation)
    keyboard = get_profile_keyboard(language)

    bot.send_message(telegramId, message_text, reply_markup=keyboard)


@handler_error_catcher()
def change_profile_handler(message: Message, telegramId: str, **kwargs) -> None:
    USERS_TMP[telegramId] = {}

    return language_display(message, telegramId)


def language_display(message: Message, telegramId: str) -> None:
    language_mode = os.getenv(ENV_LANGUAGE_MODE_KEY)

    if language_mode == LANGUAGE_MULTY_KEY:
        message_text = get_message_text(SELECT_LANGUAGE_MESSAGE, language_mode)
        keyboard = get_language_keyboard()
        msg = bot.send_message(telegramId, message_text, reply_markup=keyboard)
        return bot.register_next_step_handler(msg, language_handler)

    USERS_TMP[telegramId][LANGUAGE_KEY] = language_mode

    user = update_user(message)

    status_display(message, telegramId, user[LANGUAGE_KEY])
