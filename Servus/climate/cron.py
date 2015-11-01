# coding=utf-8
from base.utils import CJB
from plugins.utils import get_used_plugins_by_type
from .utils import command


class GetTempHumid(CJB):
    """
    CronJobBase класс для опроса датчиков температуры/влажности, подключенных к контроллеру.
    """

    RUN_EVERY_MINS = 15

    def do(self):

        th_sensors = get_used_plugins_by_type('TempHumidSensor')

        if th_sensors:
            for s in th_sensors:
                command(s, write_db=True)
