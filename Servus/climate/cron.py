# coding=utf-8
import time
import logging
from base.utils import CJB
from events.utils import event_setter
from .models import TempHumidValue
from plugins.models import PLUGIN_MODELS

logger = logging.getLogger(__name__)


def check_bad_conditions(t, h):
    """
    Проверка показаний датчика температуры и влажности на определенные условия.
    Функция нужна для многократной проверки показаний, если они превысили некоторые
    пороговые значения, т.к. датчики иногда врут, а повторный опрос происходит раз
    в 15 мин (см. RUN_EVERY_MINS).

    :param t: int Значение температуры
    :param h: int Значение влажности
    :returns: возвращает True, если показания попали за границы "нормальных"
    """

    return t > 50 or t < 0 or h < 20 or h > 90


def set_climate_event(s, h, t):
    """
    Функция записи в журнал событий данных с датчиков, находящихся за пределами нормы.
    :param s: TempHumidSensor Датчик температуры и влажности (sensor)
    :param t: int Значение температуры
    :param h: int Значение влажности    
    """

    if s.location == 'inside':
        if 28 < t <= 35 or 15 <= t < 19:
            event_setter('climate', u'%s: Температура вне нормы 19-28 С' % s.verbose_name, 2)
        elif t > 35 or t < 15:
            event_setter('climate', u'%s: Температура за границами 15-35 С' % s.verbose_name, 3, 1)
        if h < 30:
            event_setter('climate', u'%s: Воздух слишком сухой (%d%%)' % (s.verbose_name, h), 2)
        elif 60 < h:
            event_setter('climate', u'%s: Воздух слишком влажный (%d%%)' % (s.verbose_name, h), 3, 1)
    elif s.location == 'outside':
        if t > 35:
            event_setter('climate', u'%s: Температура на улице более 35 С' % s.verbose_name, 2)
        elif t < -15:
            event_setter('climate', u'%s: Температура на улице менее -15 С' % s.verbose_name, 2)


class GetTempHumid(CJB):
    """
    CronJobBase класс для опроса датчиков температуры/влажности, подключенных к контроллеру.
    """

    RUN_EVERY_MINS = 15

    def do(self):

        th_sensors = filter(lambda s: s.TYPE == 'TempHumidSensor', PLUGIN_MODELS['climate'])
        th_sensors_used = reduce(lambda res, s: res + tuple(s.objects.filter(is_used=True)), th_sensors, ())

        if th_sensors_used:
            for s in th_sensors_used:
                try:
                    c = s.controller.Command(s)
                    
                    if c.state[0]:
                        cmd = 't%d\n' % s.controller_pin
                        counter = 3
                        while counter:                        
                            result = c.send(cmd)

                            if c.state[0]:
                                h, t = map(int, result.split(':'))

                                # Проверяем полученные данные на возможные ошибки показаний.
                                # Делаем три измерения подряд с 5 секундной паузой, чтобы удостоверится, что
                                # "запредельные" значения - это не ошибка датчика
                                if check_bad_conditions(t, h):
                                    counter -= 1
                                    time.sleep(5)
                                else:
                                    TempHumidValue.objects.create(content_object=s, temperature=t, humidity=h)
                                    set_climate_event(s, h, t)
                                    break
                            else:
                                break
                    c.close_port()
                except AttributeError:
                    logger.error(u'Объект %s не имеет атрибута controller' % s)
