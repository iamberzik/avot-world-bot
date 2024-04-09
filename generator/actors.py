import io
import time
from typing import Any

from PIL import Image

from api.services import create_request
from core.conf import bot
from core.globals import FILE_PATH_KEY, USER_ID_KEY, LANGUAGE_KEY, TYPE_KEY, TEMPLATE_KEY, \
    GENERATOR_STATIC_KEY, GENERATOR_ANIMATED_KEY, TELEGRAM_ID_KEY, EXECUTION_TIME_RECORDS
from core.utils import get_debug_mode
from generator.messages import REQUEST_ERROR_MESSAGE
from generator.services import photo_generator_service, video_generator_service
from generator.utils import crop_max_square
from menu.keyboards import get_menu_keyboard


def generate_avatar_actor(worker_data: dict) -> Any:
    generator_mod_switcher = {
        GENERATOR_STATIC_KEY: photo_generator_service,
        GENERATOR_ANIMATED_KEY: video_generator_service,
    }

    telegram_id = worker_data[TELEGRAM_ID_KEY]
    language = worker_data[LANGUAGE_KEY]
    template_type = worker_data[TEMPLATE_KEY][TYPE_KEY]
    try:
        start_time = time.time()

        downloaded_file = bot.download_file(worker_data[FILE_PATH_KEY])
        image_object = Image.open(io.BytesIO(downloaded_file))
        square_avatar = crop_max_square(image_object)
        generator_mod_switcher[template_type](square_avatar, worker_data)

        execution_time = round(time.time() - start_time)
        EXECUTION_TIME_RECORDS.append(execution_time)

        create_request(worker_data)
    except Exception as e:

        if get_debug_mode():
            print(e)

        message_text = REQUEST_ERROR_MESSAGE[language]
        keyboard = get_menu_keyboard(language)
        return bot.send_message(telegram_id, message_text, reply_markup=keyboard)
