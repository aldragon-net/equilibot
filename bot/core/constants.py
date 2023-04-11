from enum import Enum

from telegram.ext import ConversationHandler


class BotState(str, Enum):
    BASE = "BASE_MENU"
    ASK_FOR_MIXTURE = "ASK_FOR_MIXTURE"
    READ_MIXTURE = "READ_MIXTURE"
    READ_PRESSURE = "READ_PRESSURE"
    CHOOSE_PARAMETER = "CHOOSE_PARAMETER"
    READ_ROOM_TEMPERATURE = "READ_ROOM_TEMPERATURE"
    READ_LENGTH = "READ_LENGTH"
    READ_TIME = "READ_TIME"
    READ_VELOCITY = "READ_VELOCITY"
    DISPLAY_RESULT = "DISPLAY_RESULT"
    STOPPING = "STOPPING"
    END = ConversationHandler.END


class CBData(str, Enum):
    MIXTURE = "MIXTURE"
    VELOCITY = "VELOCITY"
    TIME = "TIME"
    SETUP = "SETUP"
    TEMPERATURE = "TEMPERATURE"
    LENGTH = "LENGTH"
    SW2PT = "SW2PT"
    DRIVER2PT = "DRIVER2PT"
    CANCEL = "CANCEL"


class UDataKeys(str, Enum):
    MSG = "MSG"
    KBRD = "KBRD"
    REGISTERED = "REGISTERED"
    PARAMETERS = "PARAMETERS"


class ParamKeys(str, Enum):
    MIXTURE = "MIXTURE"
    P_1 = "P_1"
    T_1 = "T_1"
    U_ISW = "U_ISW"
