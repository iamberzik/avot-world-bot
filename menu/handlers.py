from telebot.types import Message

from api.decorators.handler_error_catcher import handler_error_catcher
from core.conf import bot
from core.globals import USERS_TMP
from core.utils import get_message_text, get_default_language
from menu.displays import menu_display, not_valid_display
from menu.messages import HELP_MESSAGE
from profile.handlers import language_display


@handler_error_catcher()
def not_valid_handler(message: Message, **kwargs) -> None:
    not_valid_display(message)
    start_handler(message)


@handler_error_catcher()
def start_handler(message: Message, telegramId: str, isFinished: bool, **kwargs) -> None:
    USERS_TMP[telegramId] = {}

    if isFinished:
        return menu_display(message)

    language_display(message, telegramId)


@handler_error_catcher()
def help_handler(message: Message, telegramId: str, language: str, **kwargs) -> None:
    user_language = language
    language = get_default_language(message, user_language)

    message_text = get_message_text(HELP_MESSAGE, language)

    bot.send_message(telegramId, message_text)


@handler_error_catcher()
def main_menu_handler(message: Message, **kwargs) -> None:
    menu_display(message)
