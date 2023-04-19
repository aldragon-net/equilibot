from telegram import Update
from telegram.ext import (ContextTypes, ConversationHandler,
                          CallbackQueryHandler, MessageHandler, filters)
from bot.core.constants import CBData, BotState, UDataKeys

from bot.handlers.start import start
from bot.client.clients import client


async def ask_for_setup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query is not None:
        await update.callback_query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=context.user_data[UDataKeys.MSG].ASK_FOR_SETUP.value,
        reply_markup=context.user_data[UDataKeys.KBRD].CHOOSE_PARAMETER
    )
    return BotState.CHOOSE_PARAMETER


async def ask_for_length(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query is not None:
        await update.callback_query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=context.user_data[UDataKeys.MSG].ASK_FOR_LENGTH.value,
        reply_markup=context.user_data[UDataKeys.KBRD].CANCEL
    )
    return BotState.READ_LENGTH


async def ask_for_room_temperature(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query is not None:
        await update.callback_query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=context.user_data[UDataKeys.MSG].ASK_FOR_ROOM_TEMPERATURE.value,
        reply_markup=context.user_data[UDataKeys.KBRD].CANCEL
    )
    return BotState.READ_ROOM_TEMPERATURE


async def read_length(update: Update, context: ContextTypes.DEFAULT_TYPE):
    length = update.message.text
    user_id = update.message.from_user.id
    try:
        length = float(length)
    except ValueError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=context.user_data[UDataKeys.MSG].WRONG_FORMAT.value,
        )
        return await ask_for_length(update, context)
    await ask_for_setup(update, context)
    client.update_length(user_id, length)
    return BotState.CHOOSE_PARAMETER


async def read_room_temperature(update: Update, context: ContextTypes.DEFAULT_TYPE):
    temperature_celsius = update.message.text
    user_id = update.message.from_user.id
    try:
        temperature_celsius = float(temperature_celsius)
    except ValueError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=context.user_data[UDataKeys.MSG].WRONG_FORMAT.value,
        )
        return await ask_for_room_temperature(update, context)
    temperature = temperature_celsius + 273
    client.update_temperature(user_id, temperature)
    return await ask_for_setup(update, context)


tube_setup_handler = ConversationHandler(
    name="Tube setup",
    entry_points=[CallbackQueryHandler(ask_for_setup, pattern=CBData.SETUP)],
    states={
        BotState.CHOOSE_PARAMETER: [
            CallbackQueryHandler(ask_for_length, pattern=CBData.LENGTH),
            CallbackQueryHandler(ask_for_room_temperature, pattern=CBData.TEMPERATURE)
        ],
        BotState.READ_ROOM_TEMPERATURE: [MessageHandler(filters.TEXT, read_room_temperature)],
        BotState.READ_LENGTH: [MessageHandler(filters.TEXT, read_length)]
    },
    fallbacks=[CallbackQueryHandler(start, pattern=CBData.CANCEL)],
    map_to_parent={
        BotState.BASE: BotState.BASE,
        BotState.STOPPING: BotState.END,
        BotState.END: BotState.BASE
    }
)
