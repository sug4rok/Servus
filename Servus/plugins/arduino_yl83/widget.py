# coding=utf-8
from plugins.utils import get_used_plugins_by, get_latest_sensor_value
from climate.models import RaindropValue


def rain_level(sensor, number):
    """
    Функция, определяющая 4 уровня осадков.
    Необходимо подстройка с учетом расположения, исполнения, угола наклона и пр. датчика дождя.
    Поэтому для каждого датчика записывается его исторический минимум и максимум.
    За начало осадков принято max_value - 10.

    :param sensor: plugins.models.SensorYL83 Датчик дождя
    :param number: int Число в идеальных условиях от 0 до 1023 - результат работы датчик дождя, где
    0 - полное погружение в воду, 1023 - абсолютно сухая поверхность.
    :returns: int Число от 0 до 3 - четыре уровня осадков, где 0 - осадков нет,
    3 - ливень.
    """

    min_val = sensor.min_value
    max_val = sensor.max_value
    middle_val = (max_val - min_val) / 2 + min_val
    shower_val = (max_val - min_val) / 5 + min_val

    if number <= shower_val:
        return 3
    elif shower_val < number <= middle_val:
        return 2
    elif middle_val < number <= max_val - 10:
        return 1
    else:
        return 0


def get_widget_data(plan_id):
    """
    Функция, предоставляющая данные с датчиков дождя YL-83

    :returns: list Список кортежей с данными о дожде и координатами расположения
    виджетов.
    """

    sensors = get_used_plugins_by(package='plugins.arduino_yl83')
    sensors = [s for s in sensors if s.plan_image_id == plan_id]

    values = [get_latest_sensor_value(RaindropValue, sensor) for sensor in sensors]

    return [(plan_id, v.content_object.name, v.content_object.horiz_position,
             v.content_object.vert_position, v.content_object.level,
             rain_level(v.content_object, v.raindrop)) for v in values if v is not None]
