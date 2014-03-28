# coding=utf-8
from base.cron import event_setter
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


def weather_setter(weather_data):
    """
    Функция записи массива данных, полученных с помощью функции weather_getter в таблицу weather_weather БД.
    На входе: список с данными, вида [{a1:b1, c1:d1}, {a2:b2, c2:d2},.. {an:bn, cn:dn}]
    """
    for weather in weather_data:
        obj_wp = Weather.objects.create(wp=weather['wp'])

        datetime = weather['datetime']
        obj_wp.datetime = datetime
        event_day = '%s %s' % (datetime.day, get_month(datetime.month))

        if 'clouds' in weather:
            obj_wp.clouds = int(weather['clouds'])
        if 'precipitation' in weather:
            obj_wp.precipitation = float(weather['precipitation'])

        temp = int(weather['temperature'])
        obj_wp.temperature = temp
        if 25 < temp <= 32:
            event_setter('weather', u'%s: Будет жарко (%s C)' % (event_day, temp), 2)
        elif temp > 32:
            event_setter('weather', u'%s: Будет очень жарко! (%s C)' % (event_day, temp), 3)
        elif -25 <= temp < -15:
            event_setter('weather', u'%s: Будет холодно (%s C)' % (event_day, temp), 2)
        elif temp < -25:
            event_setter('weather', u'%s: Будет очень холодно! (%s C)' % (event_day, temp), 3)

        obj_wp.pressure = int(weather['pressure'])
        obj_wp.humidity = int(weather['humidity'])

        wind_speed = int(weather['wind_speed'])
        obj_wp.wind_speed = wind_speed

        if 11 <= wind_speed < 17:
            event_setter('weather', u'%s: Сильный ветер (%s м/с)' % (event_day, wind_speed), 2)
        elif 17 <= wind_speed < 25:
            event_setter('weather', u'%s: Шторм! (%s м/с)' % (event_day, wind_speed), 3)
        elif wind_speed >= 25:
            event_setter('weather', u'%s: УРАГАН! (%s м/с)' % (event_day, wind_speed), 4)

        obj_wp.wind_direction = int(weather['wind_direction'])
        obj_wp.clouds_img = weather['clouds_img']

        falls_img = weather['falls_img']
        obj_wp.falls_img = falls_img
        if falls_img in ['t1d3', 't2d3', 't3d3']:
            event_setter('weather', u'%s: %s' % (event_day, FALLS_RANGE[falls_img]), 2)
        elif falls_img in ['t1d4', 't1d5', 't2d4', 't3d4']:
            event_setter('weather', u'%s: %s' % (event_day, FALLS_RANGE[falls_img]), 3)

        obj_wp.save()