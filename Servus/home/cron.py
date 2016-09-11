# coding=utf-8
from base.utils import CJB
from plugins.utils import get_used_plugins_by


class GetOnOffSwitchState(CJB):
    """
    CronJobBase класс для опроса переключателей с двумя состояниями кнопок,
    герконов, датчиков движения и пр., подключенных к контроллеру.
    """

    RUN_EVERY_MINS = 1

    def do(self):
        sensors = get_used_plugins_by(plugin_type='OnOffSwitch')

        if sensors:
            for sensor in sensors:
                sensor.set_command()
