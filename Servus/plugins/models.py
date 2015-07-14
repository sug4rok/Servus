# coding=utf-8
from django.db import models
from base.models import Application, Location

class Plugin(models.Model):
    """
    Модель для храенения информации о плагине
    """

    name = models.SlugField(
        verbose_name='Плагины',
        unique=True
    )
    application = models.ForeignKey(
        Application,
        verbose_name='Приложение',
        help_text='Приложение, к которому принадлежит плагин'
    )
    is_widget = models.BooleanField(
        verbose_name='Виджет',    
        help_text='Имеет собственный виджет на Главной странице',
        default=False
    )
    location = models.ForeignKey(
        Location,
        verbose_name='Расположение',
        help_text='Место расположения объекта в помещении',
    )
    is_used = models.BooleanField(
        verbose_name='Задействован',
        help_text='Выберите "Задействован", чтобы включить плагин',
        default=False
    )

    class Meta(object):
        verbose_name = 'Плагин'
        verbose_name_plural = 'Плагины'

    def __unicode__(self):
        return self.name