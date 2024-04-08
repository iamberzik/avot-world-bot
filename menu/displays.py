from telebot.types import Message

from api.services import get_or_create_user
from core.conf import bot
from core.globals import TELEGRAM_ID_KEY, LANGUAGE_KEY
from core.utils import get_default_language
from menu.keyboards import get_menu_keyboard
from menu.messages import MAIN_MENU_MESSAGE, NOT_VALID_MESSAGE


def menu_display(message: Message) -> None:
    user = get_or_create_user(message)
    user_id = user[TELEGRAM_ID_KEY]
    language = get_default_language(message, user[LANGUAGE_KEY])
    keyboard = get_menu_keyboard(language)
    message_text = MAIN_MENU_MESSAGE[language]

    bot.send_message(user_id, message_text, reply_markup=keyboard)


def not_valid_display(message) -> None:
    user = get_or_create_user(message)
    user_id = user[TELEGRAM_ID_KEY]
    language = get_default_language(message, user[LANGUAGE_KEY])
    keyboard = get_menu_keyboard(language)
    message_text = NOT_VALID_MESSAGE[language]

    bot.send_message(user_id, message_text, reply_markup=keyboard)
