# coding=utf-8
from events.utils import event_setter


def check_dht_data(temp, humid, dht_type):
    """
    Проверка показаний датчика температуры и влажности на определенные условия.
    Функция нужна для многократной проверки показаний, если они превысили некоторые
    пороговые значения, т.к. датчики иногда врут, а повторный опрос происходит раз
    в 15 мин (см. RUN_EVERY_MINS).
    Для DHT11 и DHT21: 0 < temp < 50 +-2C, 20 < humid < 80 +-5%
    Для DHT22: -40 < temp < 125 +-0.5C, 0 < humid < 100 +-5%

    :param temp: int Значение температуры
    :param humid: int Значение влажности
    :param dht_type: str Тип датчика DHT (DHT11, DHT21 или DHT22)
    :returns: возвращает True, если показания попали за границы "нормальных"
    """

    if dht_type == 'dht11' or dht_type == 'dht21':
        return temp < 50 or temp > 0 or humid > 20 or humid < 80
    else:
        return temp < 125 or temp > -40 or humid > 0 or humid < 100


def set_climate_event(sensor, humid, temp):
    """
    Функция записи в журнал событий данных с датчиков, находящихся за пределами нормы.
    :param sensor: object Датчик температуры и влажности (sensor)
    :param temp: int Значение температуры
    :param humid: int Значение влажности
    """

    if sensor.location == 'inside':
        if 28 < temp <= 35 or 15 <= temp < 19:
            event_setter('climate', u'%s: Температура вне нормы 19-28 С' % sensor.verbose_name, 2)
        elif temp > 35 or temp < 15:
            event_setter('climate', u'%s: Температура за границами 15-35 С' % sensor.verbose_name,
                         3, delay=1, email=True)
        if humid < 30:
            event_setter('climate', u'%s: Воздух слишком сухой (%d%%)' % (sensor.verbose_name, humid), 2)
        elif 60 < humid:
            event_setter('climate', u'%s: Воздух слишком влажный (%d%%)' % (sensor.verbose_name, humid),
                         3, delay=1, email=True)
    elif sensor.location == 'outside':
        if temp > 35:
            event_setter('climate', u'%s: Температура на улице более 35 С' % sensor.verbose_name, 2)
        elif temp < -15:
            event_setter('climate', u'%s: Температура на улице менее -15 С' % sensor.verbose_name, 2)
