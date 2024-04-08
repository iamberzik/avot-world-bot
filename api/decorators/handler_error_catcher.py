from typing import Callable

from api.services import get_or_create_user
from core.conf import bot
from core.globals import LANGUAGE_KEY
from core.utils import get_default_language, get_debug_mode
from generator.messages import REQUEST_ERROR_MESSAGE
from menu.buttons import MENU_BUTTON_TEXT
from menu.displays import menu_display
from menu.keyboards import get_menu_keyboard


def handler_error_catcher(debug: bool = get_debug_mode()):
    def decorator(func: Callable):

        def wrapper(*args, **kwargs):
            message = args[0]
            user = get_or_create_user(message)

            try:
                if message.text and message.text in MENU_BUTTON_TEXT.values():
                    return menu_display(message)

                kwargs = {**kwargs, **user}

                return func(*args, **kwargs)
            except Exception as e:

                if debug:
                    print(e)

                user_id = message.from_user.id
                language = get_default_language(message, user[LANGUAGE_KEY])
                keyboard = get_menu_keyboard(language)
                message_text = REQUEST_ERROR_MESSAGE[language]

                return bot.send_message(user_id, message_text, reply_markup=keyboard)

        return wrapper

    return decorator
