# coding=utf-8
from plugins.utils import get_used_plugins_by, get_latest_sensor_value
from climate.models import PressureValue


def get_widget_data(plan_id):
    """
    Функция, предоставляющая данные атмосферного давления для каждого добавленого датчика BMP085/BMP180

    :param plan_id: int ID планировки.
    :returns: list Список кортежей с данными атмосферного давления и координатами расположения.
    виджетов.
    """

    sensors = get_used_plugins_by(package='plugins.arduino_bmp085')
    sensors = [s for s in sensors if s.plan_image_id == plan_id]

    values = [get_latest_sensor_value(PressureValue, sensor) for sensor in sensors]

    return [(plan_id, v.content_object.name, v.content_object.horiz_position,
             v.content_object.vert_position, v.content_object.level,
             v.pressure) for v in values if v is not None]
