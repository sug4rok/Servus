# coding=utf-8
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class User(models.Model):
    """
    Пользователи, которым будут приходить уведомления
    """

    name = models.CharField(
        max_length=50,
        verbose_name='Имя',
    )
    email = models.EmailField(
        verbose_name='E-mail',
        blank=True,
        null=True
    )
    phone = models.BigIntegerField(
        verbose_name='Номер телефона',
        help_text='Номер телефона для отправки сообщений через сервис sms.ru.<br>\
            Диапазон номеров ограничен 1*e10 - 9,(9)*e12 (подробности на sms.ru).<br>\
            Формат для РФ 7xxxyyyyyyy, где xxx - код оператора, yyyyyyy - номер телефона.<br>',
        blank=True,
        null=True,
        validators=[
            MaxValueValidator(9999999999999),
            MinValueValidator(10000000000)
        ]
    )
    sms_ru_id = models.CharField(
        max_length=40,
        verbose_name='sms.ru api_id',
        blank=True,
        null=True
    )

    class Meta(object):
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __unicode__(self):
        return "%s's profile" % self.name


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
