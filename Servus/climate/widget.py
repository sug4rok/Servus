﻿# coding=utf-8
from django.contrib.contenttypes.models import ContentType

from plugins.utils import get_used_plugins_by
from climate.models import TempHumidValue


def get_widget_data():
    """
    Получение данных о текущей температуре и влажности из таблицы climate_temphumidvalue БД
    :returns: список кортежей вида [(<полное имя датчика>, влажность, тепмпература), ...]
    """

    th_sensors = get_used_plugins_by(type='TempHumidSensor')

    # Для каждого объекта-сенсора получаем последние данные из таблицы climate_temphumidvalue.
    # Вся сложность в определении в этой таблице пренадлежности данных конкретному сенсору, т.к.
    # для обезличивания сенсоров мы использовали GenericForeignKey.
    try:
        th_values = [TempHumidValue.objects.filter(content_type_id=ContentType.objects.get_for_model(s).id,
            object_id=s.id).order_by('-datetime')[0] for s in th_sensors]
                
        result = [(th_v.content_object.location, th_v.humidity, th_v.temperature) for th_v in th_values]
    except IndexError:
        result = []

    return {'widget_type': 'tiled', 'data': result}
