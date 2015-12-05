# coding=utf-8
from os import system
from sys import platform
from datetime import datetime

from events.utils import event_setter


def ping(host):
    """
    Простой ping. Ждем результата однопакетного пинга.
    :param host: str Сетевое имя или ip-адрес устройство.
    :returns: bool Состояние (online/offline) сетевого устройства.
    """

    if host.TYPE == 'Ping':

        response = -1
        if 'linux' in platform:
            response = system('ping -c 1 ' + host.ip_address)
        elif 'win' in platform:
            response = system('ping -n 1 -4 ' + host.ip_address)

        result = response == 0
        msg = u'%s %s' % (host.name, u'снова доступен' if result else u'больше не доступен')

        if host.online != result:
            host.online = result
            host.last_changed = datetime.now()
            host.save()
            if result:
                event_setter('system', msg, 1, email=True, delay=1)
            else:
                event_setter('system', msg, 3, email=True, delay=1)
