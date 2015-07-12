# coding=utf-8
from climate.models import TempHumidValueShort


def get_temp_humid():
    """
    Получение данных о текущей температуре и влажности из таблицы climate_temphumidvalue БД
    :returns: список кортежей вида [(<полное имя датчика>, влажность, тепмпература), ...]
    """

    th_objs = TempHumidValueShort.objects.filter(sensor__is_used=True)
    return [(th_obj.sensor.location, th_obj.humidity, th_obj.temperature) for th_obj in th_objs]


def get_widget_data():
    """
    Функция для получения данных для отображение текущего значения температуры и влажности в помещениях
    на Главной странице
    :return: list Данные с датчиков температуры и влажности
    """

    return get_temp_humid()
