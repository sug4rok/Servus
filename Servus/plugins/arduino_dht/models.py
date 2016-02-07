# coding=utf-8
from django.db import models

from plugins.arduino.models import Arduino

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
        max_length=10,
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
        unique=False,
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
