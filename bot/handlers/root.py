from telegram import Update
from telegram.ext import (ContextTypes, CommandHandler, ConversationHandler,
                          CallbackQueryHandler, MessageHandler, filters)
from bot.ui.keyboards import RuKeyboards

from bot.handlers.mixture import mixture_handler

from bot.core.constants import CBData, BotState


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "REGISTERED" not in context.user_data:
        context.user_data["REGISTERED"] = True
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Добро пожаловать в Equlib. По умолчанию используются следующие параметры:"
        )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="[параметры эксперимента]",
        reply_markup=RuKeyboards.BASE
    )
    return BotState.BASE

base_handler = ConversationHandler(
    name="Base",
    entry_points=[CommandHandler('start', start)],
    states={
        BotState.BASE: [mixture_handler],
    },
    fallbacks=[CommandHandler('start', start)],
    map_to_parent=[]
)
