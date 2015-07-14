# coding=utf-8
import time
import logging
from base.utils import CJB
from plugins.arduino.utils import Arduino
from events.utils import event_setter
from .models import TempHumidSensor, TempHumidValue, TempHumidValueShort

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
    CronJobBase класс для опроса датчиков температуры/влажности, подключенных к контроллеру arduino.
    """

    RUN_EVERY_MINS = 15

    def do(self):

        try:
            TempHumidValueShort.objects.all().delete()
        except TempHumidValue.DoesNotExist:
            pass

        sensors = TempHumidSensor.objects.filter(is_used=True)

        if sensors:
            for s in sensors:
                a = Arduino()
                if a.state[0]:
                    counter = 3
                    while counter:
                        cmd = 't%d\n' % s.arduino_pin
                        result = a.command(cmd)

                        logger.debug('Arduino: command has been received %s | result %s | state: %s ' % (cmd, result, a.state[1]))

                        if a.state[0]:                
                            h, t = map(int, result.split(':'))

                            # Проверяем полученные данные на возможные ошибки показаний.
                            # Делаем три измерения подряд с 5 секундной паузой, чтобы удостоверится, что
                            # "запредельные" значения - это не ошибка датчика
                            if check_bad_conditions(t, h):
                                counter -= 1
                                time.sleep(5)
                            else:
                                TempHumidValueShort.objects.create(sensor=s, temperature=t, humidity=h)
                                TempHumidValue.objects.create(sensor=s, temperature=t, humidity=h)
                                
                                set_climate_event(s, h, t)
                                    
                                break
                        else:
                            logger.warning(u'Климатический датчик %s: %s' % (s, a.state[1]))
                            break
                else:
                    logger.error(a.state[1])
                    event_setter('system', a.state[1], 4, 1)
                a.close_port()
