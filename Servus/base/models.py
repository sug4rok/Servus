# coding=utf-8
import re

from django.db import models
from django.forms import fields
from django.core.validators import MaxValueValidator, MinValueValidator

from home.models import Plan

WIDGET_CHOICES = (
    ('tiled', 'Плиточный'),
    ('positioned', 'Позиционный'),
)
MAC_TEMPLATE = re.compile(r'([0-9a-f]{2}[:-]){5}([0-9a-f]{2})', re.IGNORECASE)


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
        null=True,
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
    widget_type = models.SlugField(
        choices=WIDGET_CHOICES,
        default='tiled',
        verbose_name='Тип виджета',
        help_text='Для позиционного виджета укажите планировку и координаты виджета\
            в процентах от размера изображения, считая от левого верхнего угла.'
    )
    plan_image = models.ForeignKey(
        Plan,
        verbose_name='Планировка',
        null=True,
        default=None
    )
    horiz_position = models.PositiveSmallIntegerField(
        verbose_name='По горизонтали,%',
        default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ],
        blank=True
    )
    vert_position = models.PositiveSmallIntegerField(
        verbose_name='По вертикали,%',
        default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ],
        blank=True
    )

    class Meta(object):
        verbose_name = 'Приложение'
        verbose_name_plural = 'Приложения'
        ordering = ('id',)

    def __unicode__(self):
        return self.name


class MACAddressFormField(fields.RegexField):
    default_error_messages = {
        'invalid': 'Введите правильный MAC-адрес (допускаются тире и двоеточия)',
    }

    def __init__(self, *args, **kwargs):
        super(MACAddressFormField, self).__init__(MAC_TEMPLATE, *args, **kwargs)


class MACAddressField(models.Field):
    empty_strings_allowed = False

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 17
        super(MACAddressField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def formfield(self, **kwargs):
        defaults = {'form_class': MACAddressFormField}
        defaults.update(kwargs)
        return super(MACAddressField, self).formfield(**defaults)
