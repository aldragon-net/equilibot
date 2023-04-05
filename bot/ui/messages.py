from enum import Enum


class RussianMessageText(str, Enum):
    GREETING = """EquiliBot — расчет параметров ударно-нагретых потоков"""
    ASK_FOR_BASE = """Введите длину базы (в миллиметрах)"""
    ASK_FOR_ROOM_TEMPERATURE = """Введите начальную температуру (в Цельсиях)"""
