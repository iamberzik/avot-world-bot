from dotenv import load_dotenv

load_dotenv()
from generator.handlers import generator_handler
from profile.handlers import show_profile_handler, change_profile_handler
from core.globals import COMMAND_START_VALUE, COMMAND_HELP_VALUE, BOT_ID_KEY
from menu.buttons import MENU_BUTTON_TEXT, PROFILE_BUTTON_TEXT, EDIT_PROFILE_BUTTON_TEXT, GENERATE_VIDEO_BUTTON_TEXT, \
    GENERATE_AVATAR_BUTTON_TEXT

from api.conf import REQUEST_DETAILS
from menu.handlers import start_handler, help_handler, main_menu_handler, not_valid_handler

from core.conf import bot


def register_handlers():
    bot.register_message_handler(start_handler, commands=[COMMAND_START_VALUE])
    bot.register_message_handler(help_handler, commands=[COMMAND_HELP_VALUE])
    bot.register_message_handler(show_profile_handler, regexp=f'^({"|".join(PROFILE_BUTTON_TEXT.values())})$')
    bot.register_message_handler(main_menu_handler, regexp=f'^({"|".join(MENU_BUTTON_TEXT.values())})$')
    bot.register_message_handler(change_profile_handler, regexp=f'^({"|".join(EDIT_PROFILE_BUTTON_TEXT.values())})$')
    bot.register_message_handler(generator_handler,
                                 regexp=f'^({"|".join(GENERATE_VIDEO_BUTTON_TEXT.values())}|{"|".join(GENERATE_AVATAR_BUTTON_TEXT.values())})$')
    bot.register_message_handler(not_valid_handler, func=lambda message: True)


def main() -> None:
    REQUEST_DETAILS[BOT_ID_KEY] = str(bot.get_me().id)
    register_handlers()
    bot.infinity_polling()


if __name__ == '__main__':
    main()
