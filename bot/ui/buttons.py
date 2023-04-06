from enum import Enum


class EnglishButtonTexts(str, Enum):
    LANGUAGE = "🌐"
    MIXTURE = "Mixture"
    SETUP = "Setup"
    P2SW = "P4 ⇒ SW"
    SW2PT = "SW => P5/T5"
    CANCEL = "CANCEL"
    USE_VELOCITY = "Input SW velocity"
    USE_TIME = "Input time"


class RussianButtonTexts(str, Enum):
    LANGUAGE = "🌐"
    MIXTURE = "Смесь"
    SETUP = "Параметры"
    P2SW = "P4 ⇒ SW"
    SW2PT = "SW => P5/T5"
    CANCEL = "Отмена"
    USE_VELOCITY = "Ввести скорость"
    USE_TIME = "Ввести время t_base"


class Localization(Enum):
    EN = "EN"
    RU = "RU"
