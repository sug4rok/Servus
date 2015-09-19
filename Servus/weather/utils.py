# coding=utf-8
import logging
from xml.dom import minidom
from urllib2 import urlopen, HTTPError
from datetime import datetime, timedelta
from events.utils import event_setter
from weather.models import WeatherValue

logger = logging.getLogger(__name__)

CLOUDS_RANGE = {
    '0': u'Ясно',
    '1': u'Малооблачно',
    '2': u'Переменная облачность',
    '3': u'Облачно с прояснениями',
    '4': u'Облачно',
    '5': u'Пасмурная погода'
}

FALLS_RANGE = {
    't0d0': u'Без осадков',
    't1d0': u'Кратковременный дождь',
    't1d1': u'Небольшой дождь',
    't1d2': u'Дождь',
    't1d3': u'Сильный дождь',
    't1d4': u'Ливень',
    't1d5': u'Гроза',
    't2d0': u'Кратковременный мокрый снег',
    't2d1': u'Небольшой мокрый снег',
    't2d2': u'Мокрый снег',
    't2d3': u'Сильный мокрый снег',
    't2d4': u'Метель',
    't3d0': u'Кратковременный снег',
    't3d1': u'Небольшой снег',
    't3d2': u'Снег',
    't3d3': u'Сильный снег',
    't3d4': u'Метель',
    'na': u'Нет данных'
}


def file_name_prefix(d):
    """
    Функция получения приставки к файлу с картинкой в зависимости от времени суток.
    :param d: datetime Время прогноза
    :returns: str Префикс файла изображения:'cd' для дня и 'cn' - для ночи.
    """

    hours_format = '%H'
    h = int(d.strftime(hours_format))

    return 'cd' if 8 < h <= 20 else 'cn'


class WG(object):
    """
    Родительский класс для наследования схожими по инициализации работы с API прогнозных сайтов классами.
    Функция parse_to_dict реализуется в каждом классе-потомке отдельно, т.к. у каждого прогнозного сайта
    свой API и парсинг XML-данных уникален.
    """

    def __init__(self, wp):
        self.wp = wp
        self.wp_url = wp.url
        self.parsed_xml = self.parse_xml()
        self.format = '%Y-%m-%d %H:%M'

    def parse_xml(self):
        try:
            url_sock = urlopen(self.wp_url)
        except HTTPError, err:
            logger.warning(u'Weather %s: urllib2 HTTPError: %s (%s)' % (self.wp.name, err.code, err.msg))
            return -1
        try:
            parsed_xml = minidom.parse(url_sock)
            return parsed_xml
        except:
            logger.warning(u'Weather: Ошибка парсинга для %s' % self.wp.name)
            return -1
        finally:
            url_sock.close()

    def node_value_get(self, tag, node=None, subnode_num=None, attr=None):
        if node is not None:
            subnodes = node.getElementsByTagName(tag)
        else:
            subnodes = self.parsed_xml.getElementsByTagName(tag)
        if subnode_num is not None:
            if attr is not None:
                try:
                    return subnodes[subnode_num].attributes[attr].value
                except KeyError:
                    return -1
            else:
                return subnodes[subnode_num].childNodes[0].nodeValue
        else:
            return subnodes

    def __str__(self):
        return 'Weather getter class for %s weather provider' % self.wp.name


def weather_db_cleaner():
    """
    Очистка базы weather_weather перед заполнением свежими данными
    """

    try:
        WeatherValue.objects.all().delete()
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

    event_day = dt.strftime('%d %b')

    if 30 <= temp <= 35:
        event_setter('weather', u'%s: Будет жарко (выше 30 C)' % event_day, 2, delay=48)
    elif temp > 35:
        event_setter('weather', u'%s: Будет очень жарко! (выше 35 C)' % event_day, 3, email=True)
    elif -25 <= temp < -15:
        event_setter('weather', u'%s: Будет холодно (ниже -15 C)' % event_day, 2, delay=48)
    elif temp < -25:
        event_setter('weather', u'%s: Будет очень холодно! (ниже -25 C)' % event_day, 3, email=True)

    if 11 <= wind_speed < 17:
        event_setter('weather', u'%s: Сильный ветер (более 11 м/с)' % event_day, 2, delay=48)
    elif 17 <= wind_speed < 25:
        event_setter('weather', u'%s: Шторм! (скорость ветра более 17 м/с)' % event_day, 3, email=True)
    elif wind_speed >= 25:
        event_setter('weather', u'%s: УРАГАН! (скорость ветра более 25 м/с)' % event_day, 4, delay=6, sms=True, email=True)

    if falls_img in ['t1d3', 't2d3', 't3d3']:
        event_setter('weather', u'%s: %s' % (event_day, FALLS_RANGE[falls_img]), 2, delay=48)
    elif falls_img in ['t1d4', 't1d5', 't2d4', 't3d4']:
        event_setter('weather', u'%s: %s' % (event_day, FALLS_RANGE[falls_img]), 2, delay=48)


def weather_setter(weather_data):
    """
    Функция записи массива данных, полученных с помощью функции weather_getter
    в таблицу weather_weather БД.

    :param weather_data: список с данными, вида [{a1:b1, c1:d1}, {a2:b2, c2:d2},.. {an:bn, cn:dn}]
    """

    for weather in weather_data:

        dt = weather['datetime']

        if dt >= datetime.now():
            obj_wp = WeatherValue.objects.create(content_object=weather['wp'])
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
            
            
def command(wp, write_db=False):
    """
    Функция получения прогноза погоды.
    :param wp: object Поставщик прогноза погоды
    :param write_db: boolean Переменная, для переключения вывода информации - запись в базу данных / вывод в лог
    """

    if wp.TYPE == 'Forecast':
        weather_data = wp.Forecast(wp).parse_to_dict()
        
        if write_db:
            weather_setter(weather_data)
        else:
            print u'Forecast %s: result = %s' % (wp, weather_data)