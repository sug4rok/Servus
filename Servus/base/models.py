# coding=utf-8
from django.db import models


class Location(models.Model):
    """
    Место, где размещается контролируемый объект, нампример, комната, дверь, улица и пр.
    """

    name = models.CharField(
        max_length=20,
        default='',
        verbose_name='Расположение',
        help_text='Место, где размещается контролируемый объект',
        blank=True,
        unique=True
    )

    description = models.CharField(
        max_length=50,
        verbose_name='Комментарий',
        blank=True
    )

    class Meta(object):
        verbose_name = 'Расположение'
        verbose_name_plural = 'Расположения'

    def __unicode__(self):
        return self.name


class Application(models.Model):
    """
    Установленны приложения и их настройки
    """
    name = models.SlugField(
        verbose_name='Приложение',
        unique=True
    )
    is_tab = models.BooleanField(
        verbose_name='Вкладка',
        help_text='Имеет собственную вкладку в меню web-интерфейса',
        default=False
    )
    tab_name = models.CharField(
        max_length=20,
        verbose_name='Вкладка'
    )
    title = models.CharField(
        max_length=50,
        verbose_name='Заголовок',
        blank=True,
        null=True
    )
    sub_title = models.CharField(
        max_length=100,
        verbose_name='Краткое описание',
        blank=True,
        null=True
    )
    is_widget = models.BooleanField(
        verbose_name='Виджет',    
        help_text='Имеет собственный виджет на Главной странице',
        default=False
    )  

    class Meta(object):
        verbose_name = 'Приложение'
        verbose_name_plural = 'Приложения'
        ordering = ('id',)

    def __unicode__(self):
        return self.name
