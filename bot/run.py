import logging

from dotenv import dotenv_values
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (ApplicationBuilder, ContextTypes, CommandHandler,
                          CallbackQueryHandler)

from bot.ui.buttons import RussianButtonTexts as bt

# from service.schemas.models import SWProblem, SWSolution
# from service.service import isw_rsw_parameters

config = dotenv_values(".env")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    if query.data == "3":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="I'm a bot, please talk to me!",
            )

    await query.edit_message_text(text=f"Selected option: {query.data}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(bt.SETUP, callback_data="1"),
            InlineKeyboardButton(bt.MIXTURE, callback_data="2"),
            InlineKeyboardButton(bt.SW2PT, callback_data="3"),
         ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!",
        reply_markup=reply_markup)

# if __name__ == '__main__':
application = ApplicationBuilder().token(config["BOT_TOKEN"]).build()

start_handler = CommandHandler('start', start)
application.add_handler(start_handler)
application.add_handler(CallbackQueryHandler(button))

application.run_polling()
