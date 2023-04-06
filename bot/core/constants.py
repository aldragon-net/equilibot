from enum import Enum

from telegram.ext import ConversationHandler


class BotState(str, Enum):
    BASE = "BASE_MENU"
    ASK_FOR_MIXTURE = "ASK_FOR_MIXTURE"
    READ_MIXTURE = "READ_MIXTURE"
    STOPPING = "STOPPING"
    END = ConversationHandler.END


class CBData(str, Enum):
    MIXTURE = "MIXTURE"
    SETUP = "SETUP"
    SW2PT = "SW2PT"
    DRIVER2PT = "DRIVER2PT"
    CANCEL = "CANCEL"
