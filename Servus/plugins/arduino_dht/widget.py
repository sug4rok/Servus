# coding=utf-8
from django.contrib.contenttypes.models import ContentType

from plugins.utils import get_used_plugins_by
from climate.models import TempHumidValue


def get_widget_data(plan_id):
    """
    Функция, предоставляющая данные температуры и относительной влажности для каждого добавленог
    о датчика DHT.

    :returns: list Список кортежей с данными температуры, влажности и координатами расположения
    виджета.
    """

    sensors = get_used_plugins_by(package='plugins.arduino_dht')
    sensors = [s for s in sensors if s.plan_image_id == plan_id]
    try:
        values = [TempHumidValue.objects.filter(content_type_id=ContentType.objects.get_for_model(s).id,
                                                object_id=s.id).order_by('-datetime')[0] for s in sensors]

        result = [(plan_id, v.content_object.name, v.content_object.horiz_position,
                   v.content_object.vert_position, v.temperature, v.humidity) for v in values]

    except IndexError:
        result = []

    return result
