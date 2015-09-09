# coding=utf-8
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class WeatherValue(models.Model):
    """
    Модель для хранения погодных данных
    """

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    datetime = models.DateTimeField(
        verbose_name='Время прогноза',
        help_text='',
        default='2013-08-30 00:00'
    )
    clouds = models.PositiveSmallIntegerField(
        verbose_name='Облачность',
        default=0
    )
    precipitation = models.FloatField(
        max_length=4,
        verbose_name='Осадки',
        default=0.0
    )
    temperature = models.SmallIntegerField(
        verbose_name='Температура',
        help_text='°C',
        default=0
    )
    pressure = models.PositiveSmallIntegerField(
        verbose_name='Давление',
        help_text='мм рт. ст.',
        default=0
    )
    humidity = models.PositiveSmallIntegerField(
        verbose_name='Влажность',
        help_text='%',
        default=0
    )
    wind_speed = models.PositiveSmallIntegerField(
        verbose_name='Ветер',
        help_text='м/c',
        default=0
    )
    wind_direction = models.SmallIntegerField(
        verbose_name='Направление ветра',
        default=0
    )
    clouds_img = models.CharField(
        max_length=3,
        default='na'
    )
    falls_img = models.CharField(
        max_length=4,
        default='na'
    )

    def __unicode__(self):
        return '%s' % self.content_object

    class Meta(object):
        ordering = ('content_type', 'datetime')
