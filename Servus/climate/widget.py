# coding=utf-8
from plugins.utils import get_used_plugins_by, get_latest_sensor_value
from climate.models import TempHumidValue


def get_widget_data():
    """
    Получение данных о текущей температуре и влажности из таблицы climate_temphumidvalue БД
    :returns: список кортежей вида [(<полное имя датчика>, влажность, тепмпература), ...]
    """

    sensors = get_used_plugins_by(plugin_type='TempHumidSensor')
    values = [get_latest_sensor_value(TempHumidValue, sensor) for sensor in sensors]

    return [(v.content_object.location, v.humidity, v.temperature) for v in values if v is not None]
