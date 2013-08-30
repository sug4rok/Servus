# -*- coding: utf-8 -*-
from django.db import models
from base.models import Tab


class Tab_Weather(models.Model):
    app_name = models.ForeignKey(Tab)
    weather_url = models.URLField(
        verbose_name='url сайта rp5.ru',
        help_text='url на XML-API сайта rp5.ru вида http://rp5.ru/xml/XXXX/00000/ru, \
                   где XXXX - код города, для которого составляется прогноз погоды.',
        blank=True,
        null=True
    )
    
    def __unicode__(self):
        return self.weather_title

        
class RP5RU (models.Model):
    datetime = models.DateTimeField(
                                    auto_now=False,
                                    auto_now_add=False,
                                    verbose_name='Местное время',
                                    default='2013-08-30 00:00'
                                         )
    cloud_cover = models.IntegerField(
                                      max_length=2,
                                      verbose_name='Облачность',
                                      default=0
                                      )    
    falls = models.IntegerField(
                                max_length=1,
                                verbose_name='Тип осадков',
                                default=0
                                )
    precipitation = models.FloatField(
                                      max_length=4,
                                      verbose_name='Осадки',
                                      default=0.0
                                      )
    drops = models.IntegerField(
                              max_length=2,
                              verbose_name='Визуализация осадков',
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
    wind_velocity = models.IntegerField(
                                        max_length=2,
                                        verbose_name='Ветер',
                                        default=0
                                        )
    wind_direction = models.CharField(
                                      max_length=3,
                                      verbose_name='Направление ветра',
                                      default=''
                                      )      
                              
    def __unicode__(self):
	    return self.time_step