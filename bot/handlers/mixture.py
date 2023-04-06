from telegram import Update
from telegram.ext import (ContextTypes, ConversationHandler,
                          CallbackQueryHandler, MessageHandler, filters)
from bot.core.constants import CBData, BotState


async def ask_for_mixture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Введите состав смеси в формате [соединение] [мольная доля]"
    )
    return BotState.READ_MIXTURE


async def read_mixture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mixture = update.message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Новая смесь:" + mixture
    )
    return BotState.END


mixture_handler = ConversationHandler(
    name="Mixture",
    entry_points=[CallbackQueryHandler(ask_for_mixture, pattern=CBData.MIXTURE)],
    states={
        BotState.READ_MIXTURE: [MessageHandler(filters.TEXT, read_mixture)]
    },
    fallbacks=[],
    map_to_parent={
        BotState.STOPPING: BotState.END,
        BotState.END: BotState.BASE
    }
)
