# coding=utf-8
from django.contrib.contenttypes.models import ContentType

from plugins.utils import get_used_plugins_by
from climate.models import PressureValue


def get_widget_data(plan_id):
    """
    Функция, предоставляющая данные атмосферного давления для каждого добавленого датчика BMP085/BMP180

    :returns: list Список кортежей с данными атмосферного давления и координатами расположения
    виджета.
    """

    sensors = get_used_plugins_by(package='plugins.arduino_bmp085')
    sensors = [s for s in sensors if s.plan_image_id == plan_id]
    try:
        values = [PressureValue.objects.filter(content_type_id=ContentType.objects.get_for_model(s).id,
                                               object_id=s.id).order_by('-datetime')[0] for s in sensors]

        result = [(plan_id, v.content_object.name, v.content_object.horiz_position,
                   v.content_object.vert_position, v.pressure) for v in values]

    except IndexError:
        result = []

    return result
