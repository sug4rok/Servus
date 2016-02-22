# coding=utf-8
from django.contrib.contenttypes.models import ContentType

from plugins.utils import get_used_plugins_by
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

    if 500 <= number < 900: raindrop = 1
    elif 300 <= number < 500: raindrop = 2
    elif number < 300: raindrop = 3
    else: raindrop = 0

    return raindrop


def get_widget_data(plan_id):
    """
    Функция, предоставляющая данные с датчиков дождя YL-83

    :returns: list Список кортежей с данными о дожде и координатами расположения
    виджетов.
    """

    sensors = get_used_plugins_by(package='plugins.arduino_yl83')
    sensors = [s for s in sensors if s.plan_image_id == plan_id]
    try:
        values = [RaindropValue.objects.filter(content_type_id=ContentType.objects.get_for_model(s).id,
                                               object_id=s.id).order_by('-datetime')[0] for s in sensors]

        result = [(plan_id, v.content_object.name, v.content_object.horiz_position,
                   v.content_object.vert_position, rain_level(v.raindrop)) for v in values]

    except IndexError:
        result = []

    return result
