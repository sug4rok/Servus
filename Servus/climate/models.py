# coding=utf-8
from django.db import models


class TempHumidSensor(models.Model):
    """
    Модель для добавления новых датчиков влажности и температуры
    """

    sensor_name = models.CharField(
        max_length=10,
        verbose_name='Системное имя',
        unique=True
    )
    sensor_pin = models.PositiveSmallIntegerField(
        max_length=2,
        verbose_name='Вывод (pin) на Arduino',
        help_text='Для датчиков температуры выделены выводы с 2 по 5',
        unique=True,
    )
    sensor_verb_name = models.CharField(
        max_length=20,
        verbose_name='Полное имя',
        help_text='Имя, отображаемое на странице',
        blank=True
    )
    is_used = models.BooleanField(
        verbose_name='Задействован',
        help_text='Выберите "Задействован", если датчик был подключен',
        default=False
    )

    def get_sensor_name(self):
        return self.sensor_name

    def save(self, *args, **kwargs):
        if not self.sensor_verb_name:
            self.sensor_verb_name = self.get_sensor_name()
        super(TempHumidSensor, self).save(*args, **kwargs)

    class Meta(object):
        verbose_name = 'Датчик температуры'
        verbose_name_plural = 'Датчики температуры'

    def __unicode__(self):
        return self.sensor_name


class TempHumidValue(models.Model):
    """
    Модель для хранения данных, полученных с датчиков температуры и влажности
    """

    sensor_name = models.ForeignKey(TempHumidSensor)
    temperature = models.SmallIntegerField(
        max_length=3,
        verbose_name='Температура',
        default=0
    )
    humidity = models.PositiveSmallIntegerField(
        max_length=2,
        verbose_name='Влажность',
        default=0
    )
    sensor_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время замера температуры/влажности'
    )

    def __unicode__(self):
        return '%s' % self.sensor_name


class TempHumidValueShort(models.Model):
    """
    Модель для хранения текущих данных, полученных с датчиков температуры и влажности.
    В отличие от TempHumidValue хронит только последние данные.
    """

    sensor_name = models.ForeignKey(TempHumidSensor)
    temperature = models.SmallIntegerField(
        max_length=3,
        verbose_name='Температура',
        default=0
    )
    humidity = models.PositiveSmallIntegerField(
        max_length=2,
        verbose_name='Влажность',
        default=0
    )

    def __unicode__(self):
        return '%s' % self.sensor_name

