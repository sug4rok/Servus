# coding=utf-8
from base.utils import CJB
from plugins.utils import get_used_plugins_by_type
from .utils import ping


class GetPingStatus(CJB):
    """
    CronJobBase класс для ping'а сетевых устройств и записи их доступности.
    """

    RUN_EVERY_MINS = 10

    def do(self):

        hosts = get_used_plugins_by_type('Ping')

        if hosts:
            for host in hosts:
                ping(host, write_db=True)
