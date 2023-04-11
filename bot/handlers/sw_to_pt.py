from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (ContextTypes, ConversationHandler,
                          CallbackQueryHandler, MessageHandler, filters)
from bot.core.constants import CBData, BotState, UDataKeys


from bot.handlers.start import start

from bot.client.clients import client

from bot.schemas.models import SWProblem


async def get_solution(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is not None:
        user_id = update.message.from_user.id
    else:
        user_id = update.callback_query.from_user.id
    data = SWProblem(mixture=client.get_params(user_id).mixture,
                     p_1=context.user_data['p_1'],
                     T_1=client.get_params(user_id).T_1,
                     u_isw=context.user_data['u_isw'])
    solution = client.solve(data)
    text = context.user_data[UDataKeys.MSG].RESULT.format(
        T_2=solution.T_2, T_5=solution.T_5,
        p_2=solution.p_2, p_5=solution.p_5,
        n_2=solution.n_2, n_5=solution.n_5,
        u_isw=solution.u_isw, u_rsw=solution.u_rsw,
        mach_isw=solution.mach_isw, mach_rsw=solution.mach_rsw,
        a_2=solution.a_2, a_5=solution.a_5,
        density_ratio_2=solution.density_ratio_2, density_ratio_5=solution.density_ratio_5
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=context.user_data[UDataKeys.KBRD].OK
    )


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
    context.user_data['p_1'] = pressure * 1E2    # mbar -> Pa
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
    length = client.get_params(update.message.from_user.id).length
    context.user_data['u_isw'] = length / time * 1E3
    await get_solution(update, context)
    return BotState.DISPLAY_RESULT


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
        BotState.DISPLAY_RESULT: [CallbackQueryHandler(start, pattern=CBData.CANCEL)]
    },
    fallbacks=[CallbackQueryHandler(start, pattern=CBData.CANCEL)],
    map_to_parent={
        BotState.BASE: BotState.BASE,
        BotState.STOPPING: BotState.END,
        BotState.END: BotState.BASE
    }
)
