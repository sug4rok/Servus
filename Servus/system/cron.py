﻿# coding=utf-8
from base.utils import CJB
from plugins.utils import get_used_plugins_by


class PerfomArduinoCommands(CJB):
    """
    CronJobBase класс для выполнения накопившихся для контроллеров команд.
    """

    RUN_EVERY_MINS = 1

    def do(self):
        controllers = get_used_plugins_by(plugin_type='Controller')

        if controllers:
            for controller in controllers:
                controller.perform_commands()
