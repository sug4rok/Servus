# coding=utf-8
from .models import PLUGIN_MODELS


def get_plugins(type):
    """
    Функция возвращает список плагинов типа type.
    
    :param type: str Тип плагинов, напремер "Forecast".
    :returns: list Плагины типа type.
    """
    
    return filter(lambda p: p.TYPE == type, sum(PLUGIN_MODELS.values(), []))
