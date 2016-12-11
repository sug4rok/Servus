# coding=utf-8
from base.utils import CJB
from plugins.utils import get_used_plugins_by


class GetTempHumidData(CJB):
    """
    CronJobBase класс для опроса датчиков температуры и влажности.
    """

    RUN_EVERY_MINS = 5

    def do(self):
        sensors = get_used_plugins_by(plugin_type='TempHumidSensor')

        if sensors:
            for sensor in sensors:
                sensor.set_command()


class GetAmbientLightData(CJB):
    """
    CronJobBase класс для опроса датчиков освещенности.
    """

    RUN_EVERY_MINS = 1

    def do(self):
        sensors = get_used_plugins_by(plugin_type='AmbientLightSensor')

        if sensors:
            for sensor in sensors:
                sensor.set_command()


class GetPressureData(CJB):
    """
    CronJobBase класс для опроса датчиков атмосферного давления.
    """

    RUN_EVERY_MINS = 15

    def do(self):
        sensors = get_used_plugins_by(plugin_type='PressureSensor')

        if sensors:
            for sensor in sensors:
                sensor.set_command()


class GetRaindropData(CJB):
    """
    CronJobBase класс для опроса датчиков осадков.
    """

    RUN_EVERY_MINS = 1

    def do(self):
        sensors = get_used_plugins_by(plugin_type='RaindropSensor')

        if sensors:
            for sensor in sensors:
                sensor.set_command()
