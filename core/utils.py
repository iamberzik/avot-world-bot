import ast
import os
from typing import List

from telebot.types import Message

from core.globals import *
from menu.buttons import GENERATE_AVATAR_BUTTON_TEXT, GENERATE_VIDEO_BUTTON_TEXT


def get_message_text(message_text: dict, language: List[str] | str) -> str:
    if type(language) is str:
        return message_text[language]

    if len(language) > 1:
        return "\n\n".join([message_text[key] for key in language])

    return message_text[language[0]]


def get_status_or_occupation_title_by_language(item: dict, language: str) -> str:
    return item[TITLE_LANGUAGE_KEYS[language]]


def get_status_or_occupation_title_list(items: List[dict], language: str) -> List[str]:
    return [get_status_or_occupation_title_by_language(item, language) for item in items]


def get_default_language(message: Message, user_language: str = None) -> str:
    user_telegram_language = message.from_user.language_code.upper()
    system_language_list_env = os.getenv(ENV_LANGUAGES_LIST_KEY, None)
    system_language_list = ast.literal_eval(system_language_list_env)

    if user_language:
        return user_language
    elif len(system_language_list) == 1:
        return system_language_list[0]
    elif user_telegram_language in SUPPORTED_LANGUAGES.keys():
        return user_telegram_language

    return LANGUAGE_RU_KEY


def get_debug_mode() -> bool:
    return os.getenv(ENV_DEBUG_KEY, "False").lower() in ["true", 1]


def get_use_queue_mode() -> bool:
    return os.getenv(ENV_USE_QUEUE_KEY, "True").lower() in ["true", 1]


def get_generate_buttons() -> str:
    generator_mode = os.getenv(ENV_GENERATOR_MODE_KEY)

    output = []

    if generator_mode in [GENERATOR_STATIC_KEY, GENERATOR_MIX_KEY]:
        output.append("|".join(GENERATE_AVATAR_BUTTON_TEXT.values()))

    if generator_mode in [GENERATOR_ANIMATED_KEY, GENERATOR_MIX_KEY]:
        output.append("|".join(GENERATE_VIDEO_BUTTON_TEXT.values()))

    return "|".join(output)
