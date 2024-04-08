from PIL import Image, ImageDraw
from telebot.types import InputMediaPhoto, Message

from core.conf import bot
from core.globals import USERS_TMP, TEMPLATE_LIST_KEY, ID_KEY, EXECUTION_TIME_RECORDS
from generator.keyboards import get_overlay_keyboard, get_cover_keyboard
from generator.messages import LAYOUT_MESSAGE, TEMPLATE_MESSAGE, MINUTE_TEXT, SECONDS_TEXT, PHOTO_PROCESSING_MESSAGE
from redis_conf import redisQueue


def send_covers_message(telegramId: str, language: str, templates: list, template_type: str) -> Message:
    photos = []

    USERS_TMP[telegramId][TEMPLATE_LIST_KEY] = {}

    for index, template in enumerate(templates, start=1):
        template_id = template[ID_KEY]
        USERS_TMP[telegramId][TEMPLATE_LIST_KEY][str(index)] = template_id

        file = open(f'assets/{template_type.lower()}/examples/{language}/{template_id}.png', 'rb')
        photos.append(InputMediaPhoto(file))

    bot.send_media_group(telegramId, media=photos)

    message_text = TEMPLATE_MESSAGE[language]
    keyboard = get_cover_keyboard(telegramId, language)

    return bot.send_message(telegramId, message_text, reply_markup=keyboard)


def send_layovers(telegramId: str, language: str) -> Message:
    photos = []

    file = open(f'assets/overlay_examples/ABOVE.png', 'rb')
    photos.append(InputMediaPhoto(file))
    file = open(f'assets/overlay_examples/INSIDE.png', 'rb')
    photos.append(InputMediaPhoto(file))

    bot.send_media_group(telegramId, media=photos)

    message_text = LAYOUT_MESSAGE[language]
    keyboard = get_overlay_keyboard(language)

    return bot.send_message(telegramId, message_text, reply_markup=keyboard)


def get_execution_time(language: str, number_of_jobs: int):
    average_time = round(sum(EXECUTION_TIME_RECORDS) / len(EXECUTION_TIME_RECORDS))

    m, s = divmod(number_of_jobs * average_time, 60)

    return f'{m} {MINUTE_TEXT[language]} {s} {SECONDS_TEXT[language]}'


def get_execution_time_message(language: str) -> str:
    number_of_jobs = len(redisQueue) + 1
    execution_time = get_execution_time(language, number_of_jobs)

    return PHOTO_PROCESSING_MESSAGE[language].format(place=number_of_jobs, time=execution_time)


def get_file_from_message(message: Message) -> str:
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    return file_info.file_path


def crop_center(pil_img: Image, crop_width: int, crop_height: int) -> Image:
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def crop_max_square(pil_img: Image) -> Image:
    cropped = crop_center(pil_img, min(pil_img.size), min(pil_img.size))
    return cropped.resize((931, 931), Image.LANCZOS)


def get_avatar_mask(pil_img: Image) -> Image:
    mask = Image.new("L", pil_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, pil_img.size[0], pil_img.size[1]), fill=255)
    return mask


def add_photo_to_layer(result: Image, square_avatar: Image, size: tuple[int, int], position: tuple[int, int]) -> Image:
    circle_avatar = get_circle_photo(square_avatar, size, position, result.size)
    result.paste(circle_avatar, (0, 0), circle_avatar)

    return result


def get_circle_photo(square_avatar: Image, size: tuple[int, int], position: tuple[int, int],
                     original_size: tuple[int, int]) -> Image:
    user_avatar_layer = Image.new('RGBA', original_size, (0, 0, 0, 0))
    square_avatar = square_avatar.resize(size)
    mask = get_avatar_mask(square_avatar)

    user_avatar_layer.paste(square_avatar, position, mask)
    return user_avatar_layer
