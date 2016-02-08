﻿# coding=utf-8
from base.utils import CJB
from plugins.utils import get_used_plugins_by


class GetClimate(CJB):
    """
    CronJobBase класс для опроса датчиков температуры/влажности, атмосферного давления и др.,
    подключенных к контроллеру.
    """

    RUN_EVERY_MINS = 15

    def do(self):

        sensors = get_used_plugins_by(container='climate')

        if sensors:
            for sensor in sensors:
                sensor.get_data()
