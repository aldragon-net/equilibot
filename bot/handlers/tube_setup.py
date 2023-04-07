from telegram import Update
from telegram.ext import (ContextTypes, ConversationHandler,
                          CallbackQueryHandler, MessageHandler, filters)
from bot.core.constants import CBData, BotState, UDataKeys

from bot.handlers.start import start


async def ask_for_setup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=context.user_data[UDataKeys.MSG].ASK_FOR_SETUP.value,
        reply_markup=context.user_data[UDataKeys.KBRD].CHOOSE_PARAMETER
    )
    return BotState.CHOOSE_PARAMETER


async def ask_for_length(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return BotState.READ_LENGTH


async def ask_for_room_temperature(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return BotState.READ_TEMPERATURE


async def read_mixture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mixture = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=context.user_data[UDataKeys.MSG].MIXTURE_CONFIRMATION.value.format(
            mixture=mixture
        )
    )
    return BotState.END


tube_setup_handler = ConversationHandler(
    name="Tube setup",
    entry_points=[CallbackQueryHandler(ask_for_setup, pattern=CBData.SETUP)],
    states={
        BotState.CHOOSE_PARAMETER: [
            CallbackQueryHandler(ask_for_length, pattern=CBData.LENGTH),
            CallbackQueryHandler(ask_for_room_temperature, pattern=CBData.TEMPERATURE)
        ],
        BotState.READ_TEMPERATURE: [],
        BotState.READ_LENGTH: []
    },
    fallbacks=[CallbackQueryHandler(start, pattern=CBData.CANCEL)],
    map_to_parent={
        BotState.BASE: BotState.BASE,
        BotState.STOPPING: BotState.END,
        BotState.END: BotState.BASE
    }
)
