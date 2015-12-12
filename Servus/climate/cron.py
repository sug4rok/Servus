# coding=utf-8
from base.utils import CJB
from plugins.utils import get_used_plugins_by
from .utils import get_sensor_data


class GetTempHumid(CJB):
    """
    CronJobBase класс для опроса датчиков температуры/влажности, атмосферного давления и др.,
    подключенных к контроллеру.
    """

    RUN_EVERY_MINS = 15

    def do(self):

        sensors = get_used_plugins_by(plugin_type='TempHumidSensor') + \
                  get_used_plugins_by(plugin_type='PressureSensor')

        if sensors:
            for sensor in sensors:
                get_sensor_data(sensor)
