# coding=utf-8
from plugins.utils import get_used_plugins_by, get_latest_sensor_value
from climate.models import TempHumidValue


def get_widget_data(plan_id):
    """
    Функция, предоставляющая данные температуры и относительной влажности для каждого
    добавленого датчика DHT.

    :param plan_id: int ID планировки.
    :returns: list Список кортежей с данными температуры, влажности и координатами расположения
    виджета.
    """

    sensors = get_used_plugins_by(package='plugins.arduino_dht')
    sensors = [sensor for sensor in sensors if sensor.plan_image_id == plan_id]

    values = [get_latest_sensor_value(TempHumidValue, sensor) for sensor in sensors]

    return [(plan_id, v.content_object.name, v.content_object.horiz_position,
             v.content_object.vert_position, v.content_object.level,
             v.temperature, v.humidity) for v in values if v is not None]
