# coding=utf-8
from datetime import datetime, timedelta

from plugins.utils import get_used_plugins_by
from .models import WeatherValue


def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))


def nearest_forecast(plugin, begin, end, pivot):
    forecasts = WeatherValue.objects.filter(object_id=plugin.id, datetime__range=[begin, end])
    if forecasts.count():
        nearest_hour = nearest(forecasts.values_list('datetime', flat=True), pivot)
        return forecasts.get(datetime=nearest_hour)
    return None


def get_forecast(plugin, date):
    """
    Функция получения прогноза погоды на заданную дату для ночи и дня.

    :param plugin: object Объект модели плагина прогноза погоды.
    :param date: datetime День, для которого будем усреднять прогноз.
    :returns: tuple Кортеж из двух объектов с данными прогноза погоды для ночи и дня.
    """

    # Задаем граничные данные для ночи и дня (часы)
    year, month, day = date.year, date.month, date.day
    night_begin = datetime(year, month, day, 0)
    night_end = datetime(year, month, day, 5)
    day_begin = datetime(year, month, day, 10)
    day_end = datetime(year, month, day, 19)
    day_pivot = datetime(year, month, day, 12)

    return (nearest_forecast(plugin, night_begin, night_end, night_begin),
            nearest_forecast(plugin, day_begin, day_end, day_pivot))


def not_empty(data_tuple):
    return not all(item is None for item in data_tuple)


def get_widget_data():
    """
    Функция для получения данных для отображение краткой сводки прогноза погоды на сегодня и завтра
    на Главной странице.

    :return: list Погодные данные
    """

    result = []

    # Получаем все используемые модели плагинов типа 'Forecast'
    for plugin in get_used_plugins_by(plugin_type='Forecast'):
        tmp_tuple = ()

        today = get_forecast(plugin, datetime.today())
        if not_empty(today):
            tmp_tuple += (('Сегодня', today), )

        tomorrow = get_forecast(plugin, datetime.today() + timedelta(days=1))
        if not_empty(tomorrow):
            tmp_tuple += (('Завтра', tomorrow), )

        result.append((plugin, tmp_tuple))

    return result
