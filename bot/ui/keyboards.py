
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

ru_ok_markup = InlineKeyboardMarkup(
    [[InlineKeyboardButton(ru.OK, callback_data=CBData.CANCEL)]]
)

ru_use_velocity = InlineKeyboardMarkup(
    [[InlineKeyboardButton(ru.CANCEL, callback_data=CBData.CANCEL)],
     [InlineKeyboardButton(ru.USE_VELOCITY, callback_data=CBData.VELOCITY)]
     ]
)

ru_use_time = InlineKeyboardMarkup(
    [[InlineKeyboardButton(ru.CANCEL, callback_data=CBData.CANCEL),
     InlineKeyboardButton(ru.USE_TIME, callback_data=CBData.TIME)]
     ]
)

ru_use_time = InlineKeyboardMarkup(
    [[InlineKeyboardButton(ru.CANCEL, callback_data=CBData.CANCEL),
     InlineKeyboardButton(ru.USE_TIME, callback_data=CBData.TIME)]
     ]
)

ru_choose_parameter = InlineKeyboardMarkup(
    [[InlineKeyboardButton(ru.LENGTH, callback_data=CBData.LENGTH),
     InlineKeyboardButton(ru.TEMPERATURE, callback_data=CBData.TEMPERATURE)],
     [InlineKeyboardButton(ru.BACK, callback_data=CBData.CANCEL)]
     ]
)


class RuKeyboards:
    BASE = ru_base_markup
    CANCEL = ru_cancel_markup
    USE_VELOCITY = ru_use_velocity
    USE_TIME = ru_use_time
    CHOOSE_PARAMETER = ru_choose_parameter
    OK = ru_ok_markup
