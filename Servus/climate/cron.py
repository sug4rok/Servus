# coding=utf-8
from base.utils import CJB
from plugins.utils import get_plugins
from .utils import command



class GetTempHumid(CJB):
    """
    CronJobBase класс для опроса датчиков температуры/влажности, подключенных к контроллеру.
    """

    RUN_EVERY_MINS = 15

    def do(self):

        th_sensors = get_plugins('TempHumidSensor')
        th_sensors_used = reduce(lambda res, s: res + tuple(s.objects.filter(is_used=True)), th_sensors, ())

        if th_sensors_used:
            for s in th_sensors_used:
                command(s, write_db=True)
