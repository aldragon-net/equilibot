from telegram.ext import CommandHandler, ConversationHandler

from bot.handlers.start import start
from bot.handlers.mixture import mixture_handler
from bot.handlers.sw_to_pt import main_input_handler
from bot.handlers.tube_setup import tube_setup_handler

from bot.core.constants import BotState


base_handler = ConversationHandler(
    name="Base",
    entry_points=[CommandHandler('start', start)],
    states={
        BotState.BASE: [mixture_handler, main_input_handler, tube_setup_handler],
    },
    fallbacks=[CommandHandler('start', start)],
    map_to_parent=[]
)
