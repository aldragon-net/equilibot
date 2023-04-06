from telegram import Update
from telegram.ext import (ContextTypes, ConversationHandler,
                          CallbackQueryHandler, MessageHandler, filters)
from bot.core.constants import CBData, BotState


async def ask_for_pressure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Введите давление в КНД (в миллибарах)"
    )
    return BotState.READ_PRESSURE


async def read_pressure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pressure = update.message.text
    try:
        pressure = float(pressure)
    except TypeError:
        return BotState.READ_PRESSURE
    return await ask_for_time(update, context)


async def ask_for_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Введите время прохождения УВ базы (в микросекундах)"
    )
    return BotState.READ_TIME


async def read_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    time = update.message.text
    try:
        time = float(time)
    except TypeError:
        return BotState.READ_TIME
    return BotState.END


async def ask_for_velocity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Введите скорость УВ (в м/c)"
    )
    return BotState.READ_VELOCITY


async def read_velocity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    velocity = update.message.text
    try:
        velocity = float(velocity)
    except TypeError:
        return BotState.READ_VELOCITY
    return BotState.END


main_input_handler = ConversationHandler(
    name="SW to PT",
    entry_points=[CallbackQueryHandler(ask_for_pressure, pattern=CBData.SW2PT)],
    states={
        BotState.READ_PRESSURE: [MessageHandler(filters.TEXT, read_pressure)],
        BotState.READ_TIME: [MessageHandler(filters.TEXT, read_time),
                             CallbackQueryHandler(ask_for_velocity, callback=CBData.VELOCITY)],
        BotState.READ_VELOCITY: [MessageHandler(filters.TEXT, read_velocity),
                                 CallbackQueryHandler(ask_for_time, callback=CBData.TIME)],
    },
    fallbacks=[],
    map_to_parent={
        BotState.STOPPING: BotState.END,
        BotState.END: BotState.BASE
    }
)