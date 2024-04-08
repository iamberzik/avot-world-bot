from PIL import Image

from core.globals import STATUS_KEY, CODE_KEY, TEMPLATE_KEY, TEMPLATE_OVERLAY_KEY, ID_KEY, LANGUAGE_KEY, FILE_KEY, \
    TYPE_KEY, OCCUPATION_KEY, USER_OVERLAY_CHOICE_KEY, GENERATOR_OVERLAY_INSIDE_KEY, GENERATOR_OVERLAY_ABOVE_KEY
from generator.utils import add_photo_to_layer
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

    generator_photo_params = STATIC_GENERATOR_TEMPLATES[template_id]["photo_params"]
    generator_layers = STATIC_GENERATOR_TEMPLATES[template_id]["layers"]

    result = Image.open(layers_dir + generator_layers[0][FILE_KEY][language])

    for layer in generator_layers[1::]:

        if layer["type"] == "layer":
            layer_object = Image.open(layers_dir + layer["file"][language])
            result.paste(layer_object, (0, 0), layer_object)

        if layer["type"] == "occupation":
            occupation_code = worker_data[OCCUPATION_KEY][CODE_KEY]
            occupation_file = template_dir + f'occupations/{language}/{occupation_code}.png'
            layer_object = Image.open(occupation_file)
            result.paste(layer_object, (0, 0), layer_object)

        if layer["type"] == "occupation":
            status_code = worker_data[STATUS_KEY][CODE_KEY]
            occupation_file = template_dir + f'roles/{status_code}/{language}.png'
            layer_object = Image.open(occupation_file)
            result.paste(layer_object, (0, 0), layer_object)

        if layer["type"] == "photo" and not template_overlaying:
            add_photo_to_layer(result, photo, generator_photo_params["size"], generator_photo_params["position"])

        if layer["type"] == "photo" and template_overlaying and not photo_placed:

            user_overlay = worker_data[USER_OVERLAY_CHOICE_KEY]

            if user_overlay == GENERATOR_OVERLAY_INSIDE_KEY:

                add_photo_to_layer(result, photo, generator_photo_params["size"], generator_photo_params["position"])
                photo_placed = True
                continue
            elif user_overlay == GENERATOR_OVERLAY_ABOVE_KEY and not photo_skipped:

                photo_skipped = True
                continue
            else:

                add_photo_to_layer(result, photo, generator_photo_params["size"], generator_photo_params["position"])
                photo_placed = True
                continue

    return result
