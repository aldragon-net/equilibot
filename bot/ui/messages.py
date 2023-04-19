from enum import Enum


class RussianMessageText(str, Enum):
    GREETING = """EquiliBot — расчет параметров ударно-нагретых потоков.
По умолчанию используются следующие параметры:"""
    ASK_FOR_LENGTH = "Введите длину базы (в миллиметрах):"
    ASK_FOR_MIXTURE = """Введите новый состав смеси в формате
[соединение 1] [мольная доля 1] [соединение 2] [мольная доля 2]…:"""
    ASK_FOR_ROOM_TEMPERATURE = "Введите начальную температуру (в Цельсиях):"
    ASK_FOR_INITIAL_PRESSURE = "Введите давление в КНД (в миллибарах):"
    ASK_FOR_SW_VELOCITY = "Введите скорость УВ (в м/c):"
    ASK_FOR_SW_BASE_TIME = "Введите время прохождения УВ базы (в мкс):"
    ASK_FOR_SETUP = "Выберите, какой параметр вы хотите изменить"
    MIXTURE_CONFIRMATION = "Новая смесь: {mixture}"
    WRONG_FORMAT = "Ошибка формата данных. Повторите ввод."
    PARAMETERS = """Параметры эксперимента:
`Длина базы: {length:.0f} мм. Температура: {temperature_celsius:.0f} C ({temperature:.0f} К).
Смесь: {mixture}`"""
    RESULT = """Смесь `{mixture}`\.
Параметры ударно—нагретого потока:`
T₂ = {T_2:>4.0f} K       T₅ = {T_5:>4.0f} K
P₂ = {p_2:>5.2f} атм    p₅ = {p_5:>5.2f} атм
n₂ = {n_2:.1E} м⁻³  n₅ = {n_5:.1E} м⁻³
u₂ = {u_isw:>4.0f} м/c     u₅ = {u_rsw:>4.0f} м/c
M₂ = {mach_isw:.2f}         M₅ = {mach_rsw:.2f}
a₂ = {a_2:>4.0f} м/c     a₅ = {a_5:>4.0f} м/c
ρ₂/ρ₁ = {density_ratio_2:.3f}     ρ₅/ρ₁ = {density_ratio_5:.3f}`
"""
