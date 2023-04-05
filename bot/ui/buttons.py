from enum import Enum


class EnglishButtonTexts(str, Enum):
    LANGUAGE = "🌐"
    MIXTURE = "Mixture"
    SETUP = "Setup"
    P2SW = "P4 ⇒ SW"
    SW2PT = "SW => P5/T5"


class RussianButtonTexts(str, Enum):
    LANGUAGE = "🌐"
    MIXTURE = "Смесь"
    SETUP = "Параметры"
    P2SW = "P4 ⇒ SW"
    SW2PT = "SW => P5/T5"


class Localization(Enum):
    EN = "EN"
    RU = "RU"