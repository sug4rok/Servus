# coding=utf-8
import time
from datetime import datetime
from django.db import models

from climate.models import TempHumidValue
from plugins.arduino.models import Arduino, set_command
from .utils import check_dht_data, set_climate_event

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
                if check_dht_data(temp, humid, self.type):
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

                    set_climate_event(self, humid, temp)
            except ValueError:
                pass
