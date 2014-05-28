# coding=utf-8
import time
import serial
from Servus.Servus import PORT
from base.utils import event_setter, CJB
from climate.models import TempHumidSensor, TempHumidValue


class GetTempHumid(CJB):
    """
    CronJobBase класс для опроса датчиков температуры/влажности, подключенных к контроллеру arduino.
    """

    RUN_EVERY_MINS = 15

    @staticmethod
    def do():
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