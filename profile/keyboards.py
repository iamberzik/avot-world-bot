from typing import List

from telebot.types import ReplyKeyboardMarkup


def get_status_occupation_keyboard(items: List[str]) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    [keyboard.row(item) for item in items]

    return keyboard
