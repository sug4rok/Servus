# coding=utf-8
from plugins.utils import get_used_plugins_by


def get_widget_data():
    """
    Функция, для виджета plugins.system_ping, предоставляющая данные о сетевых устройствах и
    их доступность в сети.

    :returns: dict Словарь,где ключ 'data' содержит список с именами сетевых устройст и
    их состояниями (online/offline).
    """

    hosts = get_used_plugins_by(package='plugins.system_ping')

    result = [(host.name, 'glyphicon glyphicon-ok', '#62bd4f') if host.online else (
        host.name, 'glyphicon glyphicon-remove', '#ed4d63') for host in hosts]

    return {'widget_type': 'tiled', 'data': result}
