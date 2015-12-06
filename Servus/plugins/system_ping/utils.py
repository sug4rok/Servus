# coding=utf-8
from os import system
from sys import platform
import time
import logging
from datetime import datetime

from events.utils import event_setter

logger = logging.getLogger(__name__)


def ping(host):
    """
    Простой ping. Ждем результата однопакетного пинга.
    :param host: str Сетевое имя или ip-адрес устройство.
    :returns: bool Состояние (online/offline) сетевого устройства.
    """

    if host.TYPE == 'Ping':

        counter = 3
        result = True

        if 'linux' in platform:
            command = 'ping -c 1 ' + host.ip_address
        elif 'win' in platform:
            command = 'ping -n 1 -4 ' + host.ip_address
        else:
            logger.error(u'Ping: Неподдерживаемая операционная система %s', platform)

        # Делаем три пинга с 5 секундным перерывом.
        # Если все три совпадения совпадают, считаем результат окончательным.
        while counter:
            response = system(command) == 0

            if result == response:
                counter -= 1
            else:
                result = response
                counter = 2

            time.sleep(5)

        if host.online != result:
            host.online = result
            host.last_changed = datetime.now()
            host.save()

            msg = u'%s %s' % (host.name, u'снова доступен' if result else u'больше не доступен')
            if result:
                event_setter('system', msg, 1, email=True, delay=1)
            else:
                event_setter('system', msg, 3, email=True, delay=1)
