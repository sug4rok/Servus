﻿# coding=utf-8
from django.db import models
from base.models import Application, Location
from plugins.arduino.models import Arduino

MODEL = 'SensorDHT11'

LOCATION_TYPES = (
    ('inside', 'В помещении'),
    ('outside', 'На улице'),
    ('other', 'Другое'),
)


class SensorDHT11(models.Model):
    """
    Модель для добавления новых датчиков влажности и температуры DHT11
    """
    
    CONTAINER = 'climate'
    ADMIN = True
    
    name = models.SlugField(
        max_length=10,
        verbose_name='Системное имя',
        unique=True
    )
    arduino = models.ForeignKey(
        Arduino,
        verbose_name='Контроллер Arduino',
    )
    arduino_pin = models.PositiveSmallIntegerField(
        verbose_name='Вывод (pin) на Arduino',
        help_text='Для датчиков температуры выделены выводы с 2 по 5',
        unique=True,
    )
    location_type = models.SlugField(
        choices=LOCATION_TYPES,
        default='inside',
        verbose_name='Тип расположение датчика',
    )

    class Meta(object):
        verbose_name = 'Датчик DHT11'
        verbose_name_plural = 'Датчики DHT11'

    def __unicode__(self):
        return '%s: is used = %s' % (self.name, self.is_used)