# coding=utf-8
import time
from subprocess import call
from os import devnull

from django.conf import settings


def subprocess_ping(host):
    """
    Простой ping. Ждем результата однопакетного пинга.
    :param host: str Сетевое имя или ip-адрес устройство.
    :returns: bool Состояние (online/offline) сетевого устройства.
    """

    if settings.OS == 'linux':
        command = ['ping', '-c', '1', '-n', '-W', '1', '-q', host]
    elif settings.OS == 'windows':
        command = ['ping', '-n', '1', '-4', '-w', '1', host]
    else:
        return None
    return call(command, stdout=open(devnull, 'w'), stderr=open(devnull, 'w')) == 0


def triple_ping(host):
    """
    Тройной ping. Ждем результата однопакетного пинга с 5 секундным интервалом.
    Если трижды результат ping совпадает, возвращаем результат.
    :param host: str Сетевое имя или ip-адрес устройство.
    :returns: bool Состояние (online/offline) сетевого устройства.
    """

    counter = 3
    result = True

    # Делаем три пинга с 5 секундным перерывом.
    # Если все три совпадения совпадают, считаем результат окончательным.
    while counter:
        response = subprocess_ping(host)

        if result == response:
            counter -= 1
        else:
            result = response
            counter = 2

        time.sleep(5)

    return result
