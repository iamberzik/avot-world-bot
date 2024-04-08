import os

from telebot import TeleBot

from core.globals import ENV_TG_TOKEN_KEY

tg_token = os.getenv(ENV_TG_TOKEN_KEY)
bot = TeleBot(tg_token)
