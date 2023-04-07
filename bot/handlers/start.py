from telegram import Update
from telegram.ext import ContextTypes
from bot.ui.keyboards import RuKeyboards
from bot.ui.messages import RussianMessageText

from bot.core.constants import BotState, UDataKeys


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if UDataKeys.REGISTERED not in context.user_data:
        context.user_data[UDataKeys.MSG] = RussianMessageText
        context.user_data[UDataKeys.KBRD] = RuKeyboards
        context.user_data[UDataKeys.REGISTERED] = True
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=context.user_data[UDataKeys.MSG].GREETING.value
        )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="[параметры эксперимента]",
        reply_markup=context.user_data[UDataKeys.KBRD].BASE,
    )
    return BotState.BASE
