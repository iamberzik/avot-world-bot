import os
from typing import List

from telebot.types import Message

from core.globals import *


def get_message_text(message_text: dict, language: str) -> str:
    if language == LANGUAGE_MULTY_KEY:
        return f"{message_text[LANGUAGE_EN_KEY]}\n\n{message_text[LANGUAGE_RU_KEY]}"

    return message_text[language]


def get_status_or_occupation_title_by_language(item: dict, language: str) -> str:
    if language == LANGUAGE_RU_KEY:
        return item[TITLE_RU_KEY]

    if language == LANGUAGE_EN_KEY:
        return item[TITLE_EN_KEY]


def get_status_or_occupation_title_list(items: List[dict], language: str) -> List[str]:
    return [get_status_or_occupation_title_by_language(item, language) for item in items]


def get_default_language(message: Message, user_language: str = None) -> str:
    user_telegram_language = message.from_user.language_code.upper()
    system_language = os.getenv(ENV_LANGUAGE_MODE_KEY, None)

    if user_language:
        return user_language
    elif system_language != LANGUAGE_MULTY_KEY:
        return system_language
    elif user_telegram_language in [LANGUAGE_RU_KEY, LANGUAGE_EN_KEY]:
        return user_telegram_language

    return LANGUAGE_EN_KEY


def get_debug_mode() -> bool:
    return os.getenv(ENV_DEBUG_KEY, "False").lower() in ["true", 1]