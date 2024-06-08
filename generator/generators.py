from PIL import Image

from core.globals import *
from generator.utils import add_photo_to_layers
from generator_conf import STATIC_GENERATOR_TEMPLATES


def generate_static_avatar(photo: Image, worker_data: dict) -> Image:
    language = worker_data[LANGUAGE_KEY]

    template = worker_data[TEMPLATE_KEY]
    template_id = str(template[ID_KEY])
    template_overlaying = template[TEMPLATE_OVERLAY_KEY]

    template_dir = f'assets/static/templates/{template_id}/'
    layers_dir = template_dir + "layers/"

    photo_placed = False
    photo_skipped = False

    generator_photo_params = STATIC_GENERATOR_TEMPLATES[template_id][PHOTO_PARAMS_KEY]
    generator_layers = STATIC_GENERATOR_TEMPLATES[template_id][LAYERS_KEY]

    result = Image.open(layers_dir + generator_layers[0][FILE_KEY][language])

    for layer in generator_layers[1::]:

        if layer[TYPE_KEY] == LAYER_KEY:
            layer_object = Image.open(layers_dir + layer[FILE_KEY][language])
            result.paste(layer_object, (0, 0), layer_object)

        if layer[TYPE_KEY] == OCCUPATION_KEY:
            occupation_code = worker_data[OCCUPATION_KEY][CODE_KEY]
            occupation_file = template_dir + f'occupations/{language}/{occupation_code}.png'
            layer_object = Image.open(occupation_file)
            result.paste(layer_object, (0, 0), layer_object)

        if layer[TYPE_KEY] == STATUS_KEY:
            status_code = worker_data[STATUS_KEY][CODE_KEY]
            occupation_file = template_dir + f'roles/{status_code}/{language}.png'
            layer_object = Image.open(occupation_file)
            result.paste(layer_object, (0, 0), layer_object)

        if layer[TYPE_KEY] == PHOTO_KEY and not template_overlaying:
            add_photo_to_layers(result, photo, generator_photo_params[SIZE_KEY],
                                generator_photo_params[POSITION_KEY], generator_photo_params[PHOTO_SHAPE_KEY])

        if layer[TYPE_KEY] == PHOTO_KEY and template_overlaying and not photo_placed:

            user_overlay = worker_data[USER_OVERLAY_CHOICE_KEY]

            if user_overlay == GENERATOR_OVERLAY_INSIDE_KEY:

                add_photo_to_layers(result, photo, generator_photo_params[SIZE_KEY],
                                    generator_photo_params[POSITION_KEY], generator_photo_params[PHOTO_SHAPE_KEY])
                photo_placed = True
                continue
            elif user_overlay == GENERATOR_OVERLAY_ABOVE_KEY and not photo_skipped:

                photo_skipped = True
                continue
            else:

                add_photo_to_layers(result, photo, generator_photo_params[SIZE_KEY],
                                    generator_photo_params[POSITION_KEY], generator_photo_params[PHOTO_SHAPE_KEY])
                photo_placed = True
                continue

    return result
