from enum import Enum


class RussianMessageText(str, Enum):
    GREETING = """EquiliBot — расчет параметров ударно-нагретых потоков.
По умолчанию используются следующие параметры:"""
    ASK_FOR_BASE = "Введите длину базы (в миллиметрах):"
    ASK_FOR_MIXTURE = """Введите новый состав смеси в формате
[соединение 1] [мольная доля 1] [соединение 2] [мольная доля 2]…:"""
    ASK_FOR_ROOM_TEMPERATURE = "Введите начальную температуру (в Цельсиях):"
    ASK_FOR_INITIAL_PRESSURE = "Введите давление в КНД (в миллибарах):"
    ASK_FOR_SW_VELOCITY = "Введите скорость УВ (в м/c):"
    ASK_FOR_SW_BASE_TIME = "Введите время прохождения УВ базы (в мкс):"
    ASK_FOR_SETUP = "Выберите, какой параметр вы хотите изменить"
    MIXTURE_CONFIRMATION = "Новая смесь: {mixture}"
    WRONG_FORMAT = "Ошибка формата данных. Повторите ввод."
