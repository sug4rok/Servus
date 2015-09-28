# coding=utf-8
from .models import PLUGIN_MODELS


def get_plugins(type):
    """
    Функция возвращает список плагинов типа type.
    
    :param type: str Тип плагинов, напремер "Forecast".
    :returns: list Плагины типа type.
    """
    
    return filter(lambda p: p.TYPE == type, sum(PLUGIN_MODELS.values(), []))


def get_used_objects(plugins):
    """
    Функция возвращает список объектов переданных плагинов, атрибут is_used
    которых равен True.
    
    :param type: list Плагины.
    :returns: list Объекты плагинов с атрибутом is_used=True.
    """
    
    return reduce(lambda res, p: res + tuple(p.objects.filter(is_used=True)), plugins, ())
