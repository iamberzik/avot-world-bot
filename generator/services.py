import io

from PIL import Image

from core.conf import bot
from core.globals import TELEGRAM_ID_KEY, LANGUAGE_KEY, TEMPLATE_KEY, ID_KEY, TMP_IMAGE_VALUE
from generator.generators import generate_static_avatar
from generator.messages import REQUEST_SUCCESS_MESSAGE
from generator_conf import VIDEO_GENERATORS


def photo_generator_service(photo: Image, worker_data: dict) -> None:
    telegram_id = worker_data[TELEGRAM_ID_KEY]
    language = worker_data[LANGUAGE_KEY]

    result = generate_static_avatar(photo, worker_data)

    bio = io.BytesIO()
    bio.name = TMP_IMAGE_VALUE
    result.save(bio, 'png')
    bio.seek(0)

    message_caption = REQUEST_SUCCESS_MESSAGE[language]

    bot.send_photo(telegram_id, photo=bio, caption=message_caption)


def video_generator_service(photo: Image, worker_data: dict) -> None:
    telegram_id = worker_data[TELEGRAM_ID_KEY]
    language = worker_data[LANGUAGE_KEY]

    template_id = str(worker_data[TEMPLATE_KEY][ID_KEY])

    file_name = VIDEO_GENERATORS[template_id](photo, worker_data)

    with open(file_name, 'rb') as video:
        message_caption = REQUEST_SUCCESS_MESSAGE[language]
        bot.send_video(telegram_id, video=video, caption=message_caption)
