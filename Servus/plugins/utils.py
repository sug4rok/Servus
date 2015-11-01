# coding=utf-8
from .models import PLUGIN_MODELS


def get_plugins_by_type(type):
    """
    Функция возвращает список плагинов типа type.
    
    :param type: str Тип плагинов, напремер "Forecast".
    :returns: list Плагины типа type.
    """
    
    return filter(lambda p: p.TYPE == type, sum(PLUGIN_MODELS.values(), []))


def get_used_plugins(plugins):
    """
    Функция возвращает список объектов переданных плагинов, атрибут is_used
    которых равен True.
    
    :param plugins: list Плагины.
    :returns: list Объекты плагинов с атрибутом is_used=True.
    """
    
    return reduce(lambda res, p: res + tuple(p.objects.filter(is_used=True)), plugins, ())
    
    
def get_used_plugins_by_type(type):
    """
    Функция возвращает список плагинов типа type, атрибут is_used
    которых равен True.
    
    :param type: str Тип плагинов, напремер "Forecast".
    :returns: list Плагины типа type.
    """

    return get_used_plugins(get_plugins_by_type(type))
    
    
def get_widget_plugins():
    """
    Функция возвращает список плагинов, которые имеют виджеты.
    
    :returns: list Перечень плагинов-виджетов.
    """

    plugins = sum(PLUGIN_MODELS.values(), [])
    return reduce(lambda res, p: res + tuple(p.objects.filter(is_widget=True)), plugins, ())
