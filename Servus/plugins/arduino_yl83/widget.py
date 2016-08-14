# coding=utf-8
from plugins.utils import get_used_plugins_by, get_latest_sensor_value
from climate.models import RaindropValue


def rain_level(number):
    """
    Функция, определяющая 4 уровня осадков.
    Необходимо подстройка с учетом расположения, исполнения, угола наклона
    и пр. датчика дождя.

    :param number: int Число от 0 до 1023 - результат работы датчик дождя, где
    0 - полное погружение в воду, 1023 - абсолютно сухая поверхность.
    :returns: int Число от 0 до 3 - четыре уровня осадков, где 0 - осадков нет,
    3 - ливень.
    """

    if 500 <= number < 1000:
        return 1
    elif 100 <= number < 500:
        return 2
    elif number < 100:
        return 3
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
             v.content_object.vert_position, rain_level(v.raindrop)) for v in values if v is not None]
