from telebot.types import ReplyKeyboardMarkup

from core.globals import USERS_TMP, TEMPLATE_LIST_KEY
from generator.buttons import OVERLAY_ABOVE_BUTTON_TEXT, OVERLAY_UNDER_BUTTON_TEXT
from menu.buttons import MENU_BUTTON_TEXT


def get_cover_keyboard(telegramId: str, language: str) -> ReplyKeyboardMarkup:
    templates = USERS_TMP[telegramId][TEMPLATE_LIST_KEY].keys()

    keyboard = ReplyKeyboardMarkup(True, True)
    button_rows = get_keyboard_chunks(list(templates))

    for row in button_rows:
        keyboard.row(*row)

    keyboard.row(MENU_BUTTON_TEXT[language])
    return keyboard


def get_overlay_keyboard(language: str) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.row(OVERLAY_ABOVE_BUTTON_TEXT[language], OVERLAY_UNDER_BUTTON_TEXT[language])
    keyboard.row(MENU_BUTTON_TEXT[language])
    return keyboard


def get_keyboard_chunks(keys: list, row_limit: int = 5) -> list:
    output = []

    for index in range(0, len(keys), row_limit):
        output.append(keys[index:index + row_limit])

    return output
