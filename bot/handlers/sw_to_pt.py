from telegram import Update
from telegram.ext import (ContextTypes, ConversationHandler,
                          CallbackQueryHandler, MessageHandler, filters)
from bot.core.constants import CBData, BotState, UDataKeys


from bot.handlers.start import start


async def ask_for_pressure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query is not None:
        await update.callback_query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=context.user_data[UDataKeys.MSG].ASK_FOR_INITIAL_PRESSURE.value,
        reply_markup=context.user_data[UDataKeys.KBRD].CANCEL
    )
    return BotState.READ_PRESSURE


async def read_pressure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pressure = update.message.text
    try:
        pressure = float(pressure)
    except ValueError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=context.user_data[UDataKeys.MSG].WRONG_FORMAT.value,
        )
        return await ask_for_pressure(update, context)
    return await ask_for_time(update, context)


async def ask_for_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=context.user_data[UDataKeys.MSG].ASK_FOR_SW_BASE_TIME.value,
        reply_markup=context.user_data[UDataKeys.KBRD].USE_VELOCITY
    )
    return BotState.READ_TIME


async def read_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    time = update.message.text
    try:
        time = float(time)
    except ValueError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=context.user_data[UDataKeys.MSG].WRONG_FORMAT.value,
        )
        return ask_for_time(update, context)
    return BotState.END


async def ask_for_velocity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query is not None:
        await update.callback_query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=context.user_data[UDataKeys.MSG].ASK_FOR_SW_VELOCITY.value,
        reply_markup=context.user_data[UDataKeys.KBRD].USE_TIME
    )
    return BotState.READ_VELOCITY


async def read_velocity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    velocity = update.message.text
    try:
        velocity = float(velocity)
    except ValueError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=context.user_data[UDataKeys.MSG].WRONG_FORMAT.value,
        )
        return ask_for_velocity(update, context)
    return BotState.END


main_input_handler = ConversationHandler(
    name="SW to PT",
    entry_points=[CallbackQueryHandler(ask_for_pressure, pattern=CBData.SW2PT)],
    states={
        BotState.READ_PRESSURE: [MessageHandler(filters.TEXT, read_pressure)],
        BotState.READ_TIME: [MessageHandler(filters.TEXT, read_time),
                             CallbackQueryHandler(ask_for_velocity, pattern=CBData.VELOCITY)],
        BotState.READ_VELOCITY: [MessageHandler(filters.TEXT, read_velocity),
                                 CallbackQueryHandler(ask_for_time, pattern=CBData.TIME)],
    },
    fallbacks=[CallbackQueryHandler(start, pattern=CBData.CANCEL)],
    map_to_parent={
        BotState.BASE: BotState.BASE,
        BotState.STOPPING: BotState.END,
        BotState.END: BotState.BASE
    }
)
