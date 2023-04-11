from telegram import Update
from telegram.ext import ContextTypes
from bot.ui.keyboards import RuKeyboards
from bot.ui.messages import RussianMessageText

from bot.core.constants import BotState, UDataKeys

from bot.client.clients import client


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is not None:
        user_id = update.message.from_user.id
    else:
        user_id = update.callback_query.from_user.id
    if not client.is_registered(user_id):
        context.user_data[UDataKeys.MSG] = RussianMessageText
        context.user_data[UDataKeys.KBRD] = RuKeyboards
        context.user_data[UDataKeys.REGISTERED] = True
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=context.user_data[UDataKeys.MSG].GREETING.value
        )
    params = client.get_params(user_id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=context.user_data[UDataKeys.MSG].PARAMETERS.format(
            length=params.length,
            temperature=params.T_1,
            mixture=params.mixture
        ),
        reply_markup=context.user_data[UDataKeys.KBRD].BASE,
    )
    return BotState.BASE
