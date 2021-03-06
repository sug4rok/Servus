﻿# coding=utf-8
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class TempHumidValue(models.Model):
    """
    Модель для хранения данных, полученных с датчиков температуры и влажности
    """

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
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
        return '%s' % self.content_object


class PressureValue(models.Model):
    """
    Модель для хранения данных, полученных с датчиков атмосферного давления.
    """

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    pressure = models.SmallIntegerField(
        verbose_name='Атмосферное давление',
        default=0
    )
    datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время замера давления'
    )

    def __unicode__(self):
        return '%s' % self.content_object


class AmbientLightValue(models.Model):
    """
    Модель для хранения данных, полученных с датчиков освещенности
    """

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    ambient_light = models.IntegerField(
        verbose_name='Освещенность',
        default=0
    )
    datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время замера освещенности'
    )

    def __unicode__(self):
        return '%s' % self.content_object


class RaindropValue(models.Model):
    """
    Модель для хранения данных, полученных с датчиков дождя
    """

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    raindrop = models.IntegerField(
        verbose_name='Дождь',
        default=1023
    )
    datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время получения даанных'
    )

    def __unicode__(self):
        return '%s' % self.content_object
