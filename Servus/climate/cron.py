# coding=utf-8
import time
import serial
from Servus.Servus import PORT
from base.utils import event_setter, CJB
from climate.models import TempHumidSensor, TempHumidValue, TempHumidValueShort


def check_bad_conditions(t, h):
    """
    Проверка показаний датчика температуры и влажности на определенные условия.
    Функция нужна для многократной проверки показаний, если они превысили некоторые
    пороговые значения, т.к. датчики иногда врут, а повторный опрос происходит раз
    в 15 мин (см. RUN_EVERY_MINS).

    :param t: Значение температуры
    :param h: Значение влажности
    :returns: возвращает True, если показания попали за границы "нормальных"
    """

    if t > 28 or t < 19 or h < 30 or h > 60:
        return True

    return False


class GetTempHumid(CJB):
    """
    CronJobBase класс для опроса датчиков температуры/влажности, подключенных к контроллеру arduino.
    """

    RUN_EVERY_MINS = 15
    counter = 3

    def do(self):
        sensors = TempHumidSensor.objects.filter(is_used=True)
        if sensors:
            try:
                ser = serial.Serial(PORT)
                time.sleep(2)
                if ser.isOpen:
                    for s in sensors:
                        # ser.flushInput()  # flush input buffer, discarding all its contents
                        # ser.flushOutput()  # flush output buffer, aborting current output

                        ser.write('t%d\n' % s.sensor_pin)
                        time.sleep(1)
                        try:
                            ser_out = ser.readline()
                        except:
                            ser_out = ''
                        if ser_out:
                            ser_out = ser_out[:-2].split(':')
                            h, t = ser_out[0], ser_out[1]

                            if h != 'e' and t != 'e':
                                h, t = int(h), int(t)
                                TempHumidValue.objects.create(
                                    sensor_name=s,
                                    temperature=t,
                                    humidity=h
                                )
                                if check_bad_conditions(t, h) and self.counter:
                                    self.counter -= 1
                                    ser.close()
                                    self.do()
                                else:
                                    try:
                                        TempHumidValueShort.objects.all().delete()
                                    except TempHumidValue.DoesNotExist:
                                        pass
                                    TempHumidValueShort.objects.create(
                                        sensor_name=s,
                                        temperature=t,
                                        humidity=h
                                    )

                                    TempHumidValue.objects.create(
                                        sensor_name=s,
                                        temperature=t,
                                        humidity=h
                                    )
                                    if 28 < t <= 35 or 15 <= t < 19:
                                        event_setter('climate', u'%s: Температура вне нормы 19-28 С' % s.sensor_verb_name, 2)
                                    elif t > 35 or t < 15:
                                        event_setter('climate', u'%s: Температура за границами 15-35 С' % s.sensor_verb_name, 3)
                                    if h < 30:
                                        event_setter('climate', u'%s: Воздух слишком сухой' % s.sensor_verb_name, 2)
                                    elif 60 > h:
                                        event_setter('climate', u'%s: Воздух слишком влажный' % s.sensor_verb_name, 2)

                            else:
                                event_setter('climate', u'Датчик %s вернул неверные данные' % s.sensor_name, 0)
                        else:
                            event_setter('climate', u'Ошибка получения данных с %s' % s.sensor_name, 0)

                    ser.close()
            except serial.SerialException:
                event_setter('climate', u'Не могу открыть порт COM%s' % PORT, 3)