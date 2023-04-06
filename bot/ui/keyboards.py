
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.ui.buttons import RussianButtonTexts as ru

from bot.core.constants import CBData


ru_base_markup = InlineKeyboardMarkup(
    [
     [InlineKeyboardButton(ru.SETUP, callback_data=CBData.SETUP),
      InlineKeyboardButton(ru.MIXTURE, callback_data=CBData.MIXTURE),
      ],
     [InlineKeyboardButton(ru.SW2PT, callback_data=CBData.SW2PT)]
    ]
)

ru_cancel_markup = InlineKeyboardMarkup(
    [[InlineKeyboardButton(ru.CANCEL, callback_data=CBData.CANCEL)]]
)


class RuKeyboards:
    BASE = ru_base_markup
    CANCEL = ru_cancel_markup
