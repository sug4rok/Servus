# coding=utf-8
from base.utils import CJB
from plugins.utils import get_used_plugins_by
from .utils import get_temp_humid


class GetTempHumid(CJB):
    """
    CronJobBase класс для опроса датчиков температуры/влажности, подключенных к контроллеру.
    """

    RUN_EVERY_MINS = 15

    def do(self):

        th_sensors = get_used_plugins_by(plugin_type='TempHumidSensor')

        if th_sensors:
            for th_sensors in th_sensors:
                get_temp_humid(th_sensor)
