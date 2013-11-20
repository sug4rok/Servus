# -*- coding: utf-8 -*-
from django.db import models
        
        
class Weather(models.Model):
    weather_provider = models.CharField(
        max_length=3,
        verbose_name='Сайт, предоставляющий api прогноза',
        default='rp5'
    )
    datetime = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Время прогноза',
        default='2013-08-30 00:00'
    )
    clouds = models.IntegerField(
        max_length=2,
        verbose_name='Облачность',
        default=0
    )
    precipitation = models.FloatField(
        max_length=4,
        verbose_name='Осадки',
        default=0.0
    )    
    temperature = models.IntegerField(
        max_length=3,
        verbose_name='Температура',
        default=0
    )
    pressure = models.IntegerField(
        max_length=3,
        verbose_name='Давление',
        default=0
    )    
    humidity = models.IntegerField(
        max_length=2,
        verbose_name='Влажность',
        default=0
    )
    wind_speed = models.IntegerField(
        max_length=2,
        verbose_name='Ветер',
        default=0
    )
    wind_direction = models.IntegerField(
        max_length=3,
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
        return 'Forecast class for %s weather provider' % self.weather_provider
    
    class Meta:
        ordering = ('weather_provider',)