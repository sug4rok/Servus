# -*- coding: utf-8 -*-
from django.db import models
from base.models import Tab


class Tab_Weather(models.Model):
    app_name = models.ForeignKey(Tab)
    weather_url = models.URLField(
        verbose_name='url сайта rp5.ru',
        help_text='url на XML-API сайта rp5.ru вида http://rp5.ru/xml/XXXX/00000/ru, где XXXX - код города, для которого составляется прогноз погоды.',
        blank=True,
        null=True
    )
    
    def __unicode__(self):
        return self.weather_title

        
class RP5RU (models.Model):
    time_step = models.IntegerField(max_length=2, verbose_name='Временной шаг (час)')
    cloud_cover = models.IntegerField(max_length=2, verbose_name='Облачность (%)')
    precipitation = models.FloatField(max_length=4, verbose_name='Толщина осадков (мм)')
    pressure = models.IntegerField(max_length=3, verbose_name='Атмосферное давление (мм рт. ст.)')
    temperature = models.IntegerField(max_length=3, verbose_name='Температура воздуха')
    humidity = models.IntegerField(max_length=2, verbose_name='Влажность (%)')
    wind_direction = models.CharField(max_length=3, verbose_name='Направление ветра')
    wind_velocity = models.IntegerField(max_length=2, verbose_name='Скорость ветра (м/c)')
    falls = models.IntegerField(max_length=1, verbose_name='Тип осадков')
    drops = models.FloatField(max_length=2, verbose_name='Коэффициент визуализации осадков')
    
    def __unicode__(self):
	    return self.time_step