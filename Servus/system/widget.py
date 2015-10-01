# coding=utf-8
from plugins.utils import get_plugins, get_used_objects


def get_widget_data():
    """
    Функция, выводящая список сетевых устройств и их доступность в сети (ping).

    :returns: dict Словарь с именами сетевых устройст и их состояниями (online/offline).
    """

    hosts = get_used_objects(get_plugins('Ping'))
    return [(host.name, host.online) for host in hosts]

