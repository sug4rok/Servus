# coding=utf-8
from django.contrib.contenttypes.models import ContentType

from plugins.utils import get_used_plugins_by
from climate.models import TempHumidValue


def get_widget_data(plan_id):
    """
    Функция, предоставляющая данные температуры и влажности для каждого добавленого датчика DHT11

    :returns: dict Словарь,где ключ 'data' содержит список с именами сетевых устройст и
    их состояниями (online/offline).
    """

    th_sensors = get_used_plugins_by(package='plugins.arduino_dht11')
    th_sensors = [s for s in th_sensors if s.plan_image_id == plan_id]
    try:
        th_values = [TempHumidValue.objects.filter(content_type_id=ContentType.objects.get_for_model(s).id,
                                                   object_id=s.id).order_by('-datetime')[0] for s in th_sensors]

        result = [(plan_id, th_v.content_object.name, th_v.content_object.horiz_position,
                   th_v.content_object.vert_position, th_v.temperature, th_v.humidity) for th_v in th_values]

    except IndexError:
        result = []

    return result
