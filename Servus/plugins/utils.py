# coding=utf-8
from .models import PLUGIN_MODELS


def get_plugins_by_type(plugin_type):
    """
    Функция возвращает список плагинов типа plugin_type.

    :param plugin_type: str Тип плагинов, напремер "Forecast".
    :returns: list Плагины типа plugin_type.
    """

    return [p for p in sum(PLUGIN_MODELS.values(), []) if p.TYPE == plugin_type]


def get_plugins_by_package(package):
    """
    Функция возвращает список плагинов с названием модуля package.

    :param package: str Модуль плагина, например "plugins.system_ping".
    :returns: list Плагины модуля package.
    """

    return [p for p in sum(PLUGIN_MODELS.values(), []) if p.PLUGIN_PACKAGE == package]


def get_used_plugins(plugins):
    """
    Функция возвращает список объектов переданных плагинов, атрибут is_used
    которых равен True.

    :param plugins: list Плагины.
    :returns: list Объекты плагинов с атрибутом is_used=True.
    """

    return reduce(lambda res, p: res + tuple(p.objects.filter(is_used=True)), plugins, ())


def get_used_plugins_by(plugin_type=None, package=None):
    """
    Функция возвращает список плагинов с указанным типом или названим модуля, атрибут is_used
    которых равен True.

    :param plugin_type: str Тип плагинов, напремер "Forecast".
    :param package: str Модуль плагина, например "plugins.system_ping".
    :returns: list Плагины типа plugin_type.
    """

    if plugin_type is not None:
        return get_used_plugins(get_plugins_by_type(plugin_type))
    elif package is not None:
        return get_used_plugins(get_plugins_by_package(package))
    else:
        return []


def get_widget_plugin_names(widget_type):
    """
    Функция возвращает список названий модулей плагинов-виджетов.

    :param widget_type: str Тип виджета 'tiled' или 'positioned'
    """

    plugins = sum(PLUGIN_MODELS.values(), [])
    if plugins:
        return [p.PLUGIN_PACKAGE for p in plugins if p.WIDGET_TYPE == widget_type]
    return []
