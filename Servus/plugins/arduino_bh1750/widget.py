# coding=utf-8
from django.contrib.contenttypes.models import ContentType

from plugins.utils import get_used_plugins_by
from climate.models import AmbientLightValue


def get_widget_data(plan_id):
    """
    Функция, предоставляющая данные освещенности для каждого добавленого датчика BH1750

    :returns: list Список кортежей с данными освещенности и координатами расположения
    виджетов.
    """

    sensors = get_used_plugins_by(package='plugins.arduino_bh1750')
    sensors = [s for s in sensors if s.plan_image_id == plan_id]
    try:
        values = [AmbientLightValue.objects.filter(content_type_id=ContentType.objects.get_for_model(s).id,
                                                   object_id=s.id).order_by('-datetime')[0] for s in sensors]

        result = [(plan_id, v.content_object.name, v.content_object.horiz_position,
                   v.content_object.vert_position, v.ambient_light) for v in values]

    except IndexError:
        result = []

    return result
