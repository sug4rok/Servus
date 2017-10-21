# coding=utf-8
import time
from datetime import datetime
from django.db import models

from climate.models import TempHumidValue
from plugins.arduino.models import Arduino, set_command
from events.utils import event_setter

MODEL = 'SensorDHT'

DHT_TYPES = (
    ('dht11', 'DHT11'),
    ('dht21', 'DHT21'),
    ('dht22', 'DHT22'),
)

LOCATION_TYPES = (
    ('inside', 'В помещении'),
    ('outside', 'На улице'),
    ('other', 'Другое'),
)


class SensorDHT(models.Model):
    """
    Модель для добавления новых датчиков влажности и температуры DHT
    (DHT11, DHT21 и DHT22).
    """

    CONTAINER = 'climate'
    TYPE = 'TempHumidSensor'
    WIDGET_TYPE = 'positioned'

    name = models.SlugField(
        max_length=20,
        verbose_name='Системное имя',
        unique=True
    )
    type = models.SlugField(
        choices=DHT_TYPES,
        default='dht11',
        verbose_name='Тип датчика',
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
        db_table = 'climate_sensordht_ext'
        verbose_name = 'Датчик DHT'
        verbose_name_plural = 'Датчики DHT'

    def __unicode__(self):
        return self.name

    def set_command(self):
        cmd = '%s:%d\n' % (self.type, self.controller_pin)
        set_command(self, cmd)

    def set_result(self, result):
        if result is not None:
            try:
                humid, temp = map(float, result.split(':'))
                humid, temp = map(lambda x: int(round(x)), [humid, temp])

                # Проверяем полученные данные на возможные ошибки показаний.
                if self.check_dht_data(temp, humid):
                    # Добавляем данные датчика в таблицу БД только, если они отличаются от
                    # предыдущего показания, иначе обновляем время у предыдущего показания.
                    # Это сделано для более быстрой выгрузки данных для графиков, т.к.
                    # количество точек существенно сокращается.
                    try:
                        value = TempHumidValue.objects.filter(object_id=self.id).latest('id')
                    except TempHumidValue.DoesNotExist:
                        value = None
                    if value is not None and value.temperature == temp and value.humidity == humid:
                        value.datetime = datetime.now()
                        value.save()
                    else:
                        TempHumidValue.objects.create(content_object=self,
                                                      temperature=temp,
                                                      humidity=humid)

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
            if 28 < temp <= 35 or 15 <= temp < 19:
                msg = u'{0}: Температура вне нормы 19-28 С'.format(self.name)
                event_setter('climate', msg, 3)
                level = 3
            elif temp > 35 or temp < 15:
                msg = u'{0}: Температура за границами 15-35 С'.format(self.name)
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

    def check_dht_data(self, temp, humid):
        """
        Проверка показаний датчика температуры и влажности на определенные условия.
        Функция нужна для многократной проверки показаний, если они превысили некоторые
        пороговые значения, т.к. датчики иногда врут, а повторный опрос происходит раз
        в 5 мин (см. RUN_EVERY_MINS).
        Для DHT11 и DHT21: 0 < temp < 50 +-2C, 20 < humid < 80 +-5%
        Для DHT22: -40 < temp < 125 +-0.5C, 0 < humid < 100 +-5%

        :param temp: int Значение температуры
        :param humid: int Значение влажности
        :returns: возвращает True, если показания попали за границы "нормальных"
        """

        if self.type == 'dht11' or self.type == 'dht21':
            return temp < 50 or temp > 0 or humid > 20 or humid < 80
        else:
            return temp < 125 or temp > -40 or humid > 0 or humid < 100
