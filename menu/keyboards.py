import os

from telebot.types import ReplyKeyboardMarkup

from core.globals import ENV_GENERATOR_MODE_KEY, GENERATOR_STATIC_KEY, GENERATOR_MIX_KEY, \
    GENERATOR_ANIMATED_KEY, SUPPORTED_LANGUAGES
from menu.buttons import *


def get_menu_keyboard(language: str) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

    buttons = []

    generator_mode = os.getenv(ENV_GENERATOR_MODE_KEY)

    if generator_mode == GENERATOR_MIX_KEY:
        buttons.append(GENERATE_AVATAR_BUTTON_TEXT[language])
        buttons.append(GENERATE_VIDEO_BUTTON_TEXT[language])
    elif generator_mode == GENERATOR_STATIC_KEY:
        buttons.append(GENERATE_AVATAR_BUTTON_TEXT[language])
    elif generator_mode == GENERATOR_ANIMATED_KEY:
        buttons.append(GENERATE_VIDEO_BUTTON_TEXT[language])

    buttons.append(PROFILE_BUTTON_TEXT[language])

    keyboard.row(*buttons)

    return keyboard


def get_language_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row(*SUPPORTED_LANGUAGES.values())
    return keyboard


def get_back_keyboard(language: str) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row(MENU_BUTTON_TEXT[language])
    return keyboard


def get_profile_keyboard(language: str) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row(EDIT_PROFILE_BUTTON_TEXT[language], MENU_BUTTON_TEXT[language])
    return keyboard
