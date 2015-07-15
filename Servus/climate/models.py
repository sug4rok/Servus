# coding=utf-8
from django.db import models
from base.models import Location

LOCATION_TYPES = (
    ('inside', 'В помещении'),
    ('outside', 'На улице'),
    ('other', 'Другое'),
)
    
    
class TempHumidSensor(models.Model):
    """
    Модель для добавления новых датчиков влажности и температуры
    """

    name = models.SlugField(
        max_length=10,
        verbose_name='Системное имя',
        unique=True
    )
    arduino_pin = models.PositiveSmallIntegerField(
        verbose_name='Вывод (pin) на Arduino',
        help_text='Для датчиков температуры выделены выводы с 2 по 5',
        unique=True,
    )
    location = models.ForeignKey(
        Location,
        verbose_name='Расположение',
        help_text='Расположение датчика',
    )
    location_type = models.SlugField(
        choices=LOCATION_TYPES,
        default='inside',
        verbose_name='Тип расположение датчика',
    )
    is_used = models.BooleanField(
        verbose_name='Задействован',
        help_text='Выберите "Задействован", если датчик был подключен',
        default=False
    )

    class Meta(object):
        verbose_name = 'Датчик температуры'
        verbose_name_plural = 'Датчики температуры'

    def __unicode__(self):
        return self.name


class TempHumidValue(models.Model):
    """
    Модель для хранения данных, полученных с датчиков температуры и влажности
    """

    sensor = models.ForeignKey(TempHumidSensor)
    temperature = models.SmallIntegerField(
        verbose_name='Температура',
        default=0
    )
    humidity = models.PositiveSmallIntegerField(
        verbose_name='Влажность',
        default=0
    )
    datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время замера температуры/влажности'
    )

    def __unicode__(self):
        return '%s' % self.sensor

