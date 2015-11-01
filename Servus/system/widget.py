# coding=utf-8
from plugins.utils import get_used_plugins_by_type


def get_widget_data():
    """
    Функция, выводящая список сетевых устройств и их доступность в сети (ping).

    :returns: dict Словарь с именами сетевых устройст и их состояниями (online/offline).
    """

    hosts = get_used_plugins_by_type('Ping')
    
    return [(host.name, 'glyphicon glyphicon-ok', '#62bd4f') if host.online else (
        host.name, 'glyphicon glyphicon-remove', '#ed4d63') for host in hosts]
