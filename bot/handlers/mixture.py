from telegram import Update
from telegram.ext import (ContextTypes, ConversationHandler,
                          CallbackQueryHandler, MessageHandler, filters)
from bot.core.constants import CBData, BotState, UDataKeys
from bot.handlers.start import start
from bot.client.clients import client


class MixtureValidationError(Exception):
     pass


def validate_mixture(mixture: str) -> str:
    items = mixture.strip().split()
    if len(items) % 2 != 0:
        raise MixtureValidationError
    print(items)
    n = len(items) // 2
    normalized_mixture = []
    for i in range(n):
        species = items[i*2]
        fraction = items[i*2 + 1]
        if species.isdigit():
            raise MixtureValidationError
        try:
            float(fraction)
        except ValueError:
            raise MixtureValidationError
        normalized_mixture.append(":".join([species.upper(), fraction]))
    return ' '.join(normalized_mixture)


async def ask_for_mixture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=context.user_data[UDataKeys.MSG].ASK_FOR_MIXTURE.value
    )
    return BotState.READ_MIXTURE


async def read_mixture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mixture = update.message.text
    user_id = update.message.from_user.id
    try:
        mixture = validate_mixture(mixture)
    except MixtureValidationError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❗ Ошибка, повторите ввод"
        )
        return await ask_for_mixture(update, context)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=context.user_data[UDataKeys.MSG].MIXTURE_CONFIRMATION.value.format(
            mixture=mixture
        )
    )
    client.update_mixture(user_id, mixture)
    await start(update, context)
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
