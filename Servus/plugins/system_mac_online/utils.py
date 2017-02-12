# coding=utf-8
import socket
from subprocess import Popen, PIPE
import re

from plugins.system_ip_online.utils import subprocess_ping

MAC_TEMPLATE = re.compile(r'([0-9a-f]{2}[:-]){5}([0-9a-f]{2})', re.IGNORECASE)


def current_ip():
    """
    Определение текущего IP-адреса.
    :returns: str Текущий IP-адрес.
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('8.8.8.8', 0))
    return sock.getsockname()[0]


def pool_ips(start_ip, end_ip, curr_ip):
    """
    Получение списка IP-адресов из той же локальной сети, что и указанный в
    параметре IP-адрес (упрощенно: берем первые 3 октета).
    :param start_ip: int Начальный адрес.
    :param end_ip: int Конечный адрес.
    :param curr_ip: str Текущий IP-адрес.
    :returns: list Список IP-адресов.
    """

    network = curr_ip.rpartition('.')[0] + '.'
    return [network + str(i) for i in xrange(start_ip, end_ip)]


def get_mac(ip):
    """
    Определение MAC-адреса для указанного IP-адреса. Вначале выполняем ping, чтобы
    в таблице ARP появилась запись для данного IP-адреса.
    :param ip: str IP-адрес.
    :returns: str MAC-адрес.
    """

    subprocess_ping(ip)

    process = Popen(['arp', '-a', ip], stdout=PIPE)
    arp = process.communicate()[0]
    mac = MAC_TEMPLATE.search(arp)

    if mac:
        return mac.group().replace('-', ':')
    return None
