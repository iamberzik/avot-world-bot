from telebot.types import Message

from api.decorators.handler_error_catcher import handler_error_catcher
from api.services import get_all_static_templates_by_bot, get_all_animated_templates_by_bot
from api.services import get_template_by_id
from core.conf import bot
from core.globals import *
from core.utils import get_use_queue_mode
from generator.actors import generate_avatar_actor
from generator.buttons import OVERLAY_UNDER_BUTTON_TEXT, OVERLAY_ABOVE_BUTTON_TEXT, OVERLAY_IN_LANGUAGES
from generator.keyboards import get_cover_keyboard
from generator.keyboards import get_overlay_keyboard
from generator.messages import LAYOUT_MESSAGE, PHOTO_PROCESSING_WITHOUT_QUEUE
from generator.messages import TEMPLATE_MESSAGE, PHOTO_REQUEST_MESSAGE
from generator.utils import send_covers_message, get_file_from_message, send_layovers, get_execution_time_message
from menu.buttons import GENERATE_AVATAR_BUTTON_TEXT, GENERATE_VIDEO_BUTTON_TEXT
from menu.keyboards import get_back_keyboard, get_menu_keyboard
from redis_conf import redisQueue


@handler_error_catcher()
def generator_handler(message: Message, telegramId: str, language: str, **kwargs) -> None:
    USERS_TMP[telegramId] = {}

    template_display(telegramId, language, message.text)


def template_display(telegramId: str, language: str, message_text: str) -> None:
    templates_switcher = {
        GENERATE_AVATAR_BUTTON_TEXT[language]: {
            TEMPLATES_SWITCHER_KEY: get_all_static_templates_by_bot,
            TYPE_KEY: GENERATOR_STATIC_KEY
        },
        GENERATE_VIDEO_BUTTON_TEXT[language]: {
            TEMPLATES_SWITCHER_KEY: get_all_animated_templates_by_bot,
            TYPE_KEY: GENERATOR_ANIMATED_KEY
        },
    }

    templates = templates_switcher[message_text][TEMPLATES_SWITCHER_KEY]()
    template_type = templates_switcher[message_text][TYPE_KEY]

    if len(templates) > 1:
        msg = send_covers_message(telegramId, language, templates, template_type)
        return bot.register_next_step_handler(msg, template_handler)

    USERS_TMP[telegramId][TEMPLATE_KEY] = templates[0]
    overlay_display(telegramId, language)


@handler_error_catcher()
def template_handler(message: Message, telegramId: str, language: str, **kwargs) -> None:
    if not message.text or (message.text and not message.text.isdigit()):
        keyboard = get_cover_keyboard(telegramId, language)
        message_text = TEMPLATE_MESSAGE[language]

        msg = bot.send_message(telegramId, message_text, reply_markup=keyboard)
        return bot.register_next_step_handler(msg, template_handler)

    template = get_template_by_id(message.text)
    USERS_TMP[telegramId][TEMPLATE_KEY] = template

    overlay_display(telegramId, language)


def overlay_display(telegramId: str, language: str) -> None:
    template = USERS_TMP[telegramId][TEMPLATE_KEY]

    if template[TEMPLATE_OVERLAY_KEY]:
        msg = send_layovers(telegramId, language)
        return bot.register_next_step_handler(msg, overlay_handler)

    USERS_TMP[telegramId][USER_OVERLAY_CHOICE_KEY] = GENERATOR_OVERLAY_ABOVE_KEY

    generation_request_display(telegramId, language)


@handler_error_catcher()
def overlay_handler(message: Message, telegramId: str, language: str, **kwargs) -> None:
    if not message.text or message.text not in [OVERLAY_UNDER_BUTTON_TEXT[language],
                                                OVERLAY_ABOVE_BUTTON_TEXT[language]]:
        keyboard = get_overlay_keyboard(language)
        message_text = LAYOUT_MESSAGE[language]
        msg = bot.send_message(telegramId, message_text, reply_markup=keyboard)
        return bot.register_next_step_handler(msg, overlay_handler)

    USERS_TMP[telegramId][USER_OVERLAY_CHOICE_KEY] = OVERLAY_IN_LANGUAGES[message.text]

    generation_request_display(telegramId, language)


def generation_request_display(telegramId: str, language: str) -> None:
    message_text = PHOTO_REQUEST_MESSAGE[language]
    keyboard = get_back_keyboard(language)

    msg = bot.send_message(telegramId, message_text, reply_markup=keyboard)
    bot.register_next_step_handler(msg, generation_request_handler)


@handler_error_catcher()
def generation_request_handler(message: Message, telegramId: str, language: str, occupation: dict, status: dict,
                               **kwargs) -> None:
    if not message.photo:
        message_text = PHOTO_REQUEST_MESSAGE[language]
        keyboard = get_back_keyboard(language)

        msg = bot.send_message(telegramId, message_text, reply_markup=keyboard)
        return bot.register_next_step_handler(msg, generation_request_handler)

    request_data = {
        TELEGRAM_ID_KEY: telegramId,
        FILE_PATH_KEY: get_file_from_message(message),
        TEMPLATE_KEY: USERS_TMP[telegramId][TEMPLATE_KEY],
        USER_OVERLAY_CHOICE_KEY: USERS_TMP[telegramId][USER_OVERLAY_CHOICE_KEY],
        OCCUPATION_KEY: occupation,
        STATUS_KEY: status,
        LANGUAGE_KEY: language
    }

    if get_use_queue_mode():

        redisQueue.enqueue(generate_avatar_actor, request_data)

        message_text = get_execution_time_message(language)
        keyboard = get_menu_keyboard(language)

        bot.send_message(telegramId, message_text, reply_markup=keyboard)

    else:
        message_text = PHOTO_PROCESSING_WITHOUT_QUEUE[language]
        keyboard = get_menu_keyboard(language)
        bot.send_message(telegramId, message_text, reply_markup=keyboard)

        generate_avatar_actor(request_data)
