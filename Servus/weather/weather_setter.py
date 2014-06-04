# coding=utf-8
from datetime import datetime
from base.utils import event_setter
from weather.models import Weather
from weather.views import FALLS_RANGE
from base.views import get_month


def weather_db_cleaner():
    """
    Очистка базы weather_weather перед заполнением свежими данными
    """

    try:
        Weather.objects.all().delete()
    except Weather.DoesNotExist:
        pass


def set_weather_events(dt, temp, wind_speed, falls_img):
    """
    Функция записи событий о прогнозируемых экстремальных погодных условиях.

    :param dt: объект datetime с датой потенциального события
    :param temp: температура воздуха
    :param wind_speed: скорость ветра
    :param falls_img: возможное количество осадков (см. weather_getter.py)
    """

    event_day = '%s %s' % (dt.day, get_month(dt.month))

    if 30 <= temp <= 35:
        event_setter('weather', u'%s: Будет жарко (выше 30 C)' % event_day, 2, 48)
    elif temp > 35:
        event_setter('weather', u'%s: Будет очень жарко! (выше 35 C)' % event_day, 2, 48)
    elif -25 <= temp < -15:
        event_setter('weather', u'%s: Будет холодно (ниже -15 C)' % event_day, 2, 48)
    elif temp < -25:
        event_setter('weather', u'%s: Будет очень холодно! (ниже -25 C)' % event_day, 2, 48)

    if 11 <= wind_speed < 17:
        event_setter('weather', u'%s: Сильный ветер (более 11 м/с)' % event_day, 2, 48)
    elif 17 <= wind_speed < 25:
        event_setter('weather', u'%s: Шторм! (скорость ветра более 17 м/с)' % event_day, 2)
    elif wind_speed >= 25:
        event_setter('weather', u'%s: УРАГАН! (скорость ветра более 25 м/с)' % event_day, 3, 6)

    if falls_img in ['t1d3', 't2d3', 't3d3']:
        event_setter('weather', u'%s: %s' % (event_day, FALLS_RANGE[falls_img]), 2, 48)
    elif falls_img in ['t1d4', 't1d5', 't2d4', 't3d4']:
        event_setter('weather', u'%s: %s' % (event_day, FALLS_RANGE[falls_img]), 2, 48)


def weather_setter(weather_data):
    """
    Функция записи массива данных, полученных с помощью функции weather_getter
    в таблицу weather_weather БД.

    :param weather_data: список с данными, вида [{a1:b1, c1:d1}, {a2:b2, c2:d2},.. {an:bn, cn:dn}]
    """

    for weather in weather_data:

        dt = weather['datetime']

        if dt >= datetime.now():
            obj_wp = Weather.objects.create(wp=weather['wp'])
            obj_wp.datetime = dt

            if 'clouds' in weather:
                obj_wp.clouds = int(weather['clouds'])
            if 'precipitation' in weather:
                obj_wp.precipitation = float(weather['precipitation'])

            temp = int(weather['temperature'])
            obj_wp.temperature = temp

            obj_wp.pressure = int(weather['pressure'])
            obj_wp.humidity = int(weather['humidity'])

            wind_speed = int(weather['wind_speed'])
            obj_wp.wind_speed = wind_speed

            obj_wp.wind_direction = int(weather['wind_direction'])
            obj_wp.clouds_img = weather['clouds_img']

            falls_img = weather['falls_img']
            obj_wp.falls_img = falls_img

            obj_wp.save()

            set_weather_events(dt, temp, wind_speed, falls_img)