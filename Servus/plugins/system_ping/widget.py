# coding=utf-8
from plugins.utils import get_used_plugins_by


def get_widget_data():
    """ Функция, для виджета plugins.system_ping, возвращающая словарь с объектами сетевых устройств. """

    return get_used_plugins_by(package='plugins.system_ping')
