# coding=utf-8
import time
from datetime import datetime
from django.db import models

from climate.models import TempHumidValue
from plugins.arduino.models import Arduino, set_command
from events.utils import event_setter

MODEL = 'SensorDS18D20'

LOCATION_TYPES = (
    ('inside', 'В помещении'),
    ('outside', 'На улице'),
    ('other', 'Другое'),
)


class SensorDS18D20(models.Model):
    """
    Модель для добавления новых датчиков температуры DS18D20.
    """

    CONTAINER = 'climate'
    TYPE = 'TempHumidSensor'
    WIDGET_TYPE = 'positioned'

    name = models.SlugField(
        max_length=20,
        verbose_name='Системное имя',
        unique=True
    )
    controller = models.ForeignKey(
        Arduino,
        verbose_name='Контроллер Arduino',
    )
    controller_pin = models.PositiveSmallIntegerField(
        verbose_name='Вывод (pin) на Arduino',
    )
    location_type = models.SlugField(
        choices=LOCATION_TYPES,
        default='inside',
        verbose_name='Тип расположение датчика',
    )

    class Meta(object):
        db_table = 'climate_sensords18d20_ext'
        verbose_name = 'Датчик DS18D20'
        verbose_name_plural = 'Датчики DS18D20'

    def __unicode__(self):
        return self.name

    def set_command(self):
        cmd = 'ds18d20:%d' % (self.controller_pin,)
        set_command(self, cmd)

    def set_result(self, result):
        if result is not None:
            try:
                temp = int(result)
                # Проверяем полученные данные на возможные ошибки показаний.
                if self.check_data(temp):
                    # Добавляем данные датчика в таблицу БД только, если они отличаются от
                    # предыдущего показания, иначе обновляем время у предыдущего показания.
                    # Это сделано для более быстрой выгрузки данных для графиков, т.к.
                    # количество точек существенно сокращается.
                    try:
                        value = TempHumidValue.objects.filter(object_id=self.id).latest('id')
                    except TempHumidValue.DoesNotExist:
                        value = None
                    if value is not None and value.temperature == temp:
                        value.datetime = datetime.now()
                        value.save()
                    else:
                        TempHumidValue.objects.create(content_object=self,
                                                      temperature=temp,
                                                      humidity=0)

                    self.set_event(temp)
            except ValueError:
                pass

    def set_event(self, temp):
        """
        Запись в журнал событий данных, находящихся за пределами нормы.
        :param temp: int Значение температуры
        """

        level = 2
        if self.location_type == 'inside':
            if 28 < temp <= 40 or 13 <= temp < 18:
                msg = u'{0}: Температура вне нормы 18-28 С'.format(self.name)
                event_setter('climate', msg, 3)
                level = 3
            elif temp > 40 or temp < 13:
                msg = u'{0}: Температура за границами 13-40 С'.format(self.name)
                event_setter('climate', msg, 4, email=True)
                level = 4

        elif self.location_type == 'outside':
            if temp > 35:
                msg = u'{0}: Температура на улице более 35 С'.format(self.name)
                event_setter('climate', msg, 3)
                level = 3
            elif temp < -15:
                msg = u'{0}: Температура на улице менее -15 С'.format(self.name)
                event_setter('climate', msg, 3)
                level = 3

        self.level = level
        self.save()

    def check_data(self, temp):
        """
        Проверка показаний датчика температуры и влажности на определенные условия.
        Функция нужна для многократной проверки показаний, если они превысили некоторые
        пороговые значения, т.к. датчики иногда врут, а повторный опрос происходит раз
        в 5 мин (см. RUN_EVERY_MINS).
        Для DS18D20: -55 < temp < 125 +-0.5C

        :param temp: int Значение температуры
        :returns: возвращает True, если показания попали за границы "нормальных"
        """

        return temp < 125 or temp > -55
