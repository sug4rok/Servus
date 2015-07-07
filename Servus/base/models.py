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


class Tab(models.Model):
    """
    Вкладки и связанные с ними типы приложений
    """

    app_name = models.SlugField(
        max_length=20,
        default='home',
        verbose_name='Тип приложения',
    )
    tab_name = models.CharField(
        max_length=20,
        verbose_name='Вкладка'
    )
    title = models.CharField(
        max_length=50,
        verbose_name='Заголовок'
    )
    sub_title = models.CharField(
        max_length=100,
        verbose_name='Краткое описание',
        blank=True,
        null=True
    )

    is_shown = models.BooleanField(
        verbose_name='Включена',
        help_text='Отображение/Скрытие вкладки (необходим перезапуск web-сервера)',
        default=False
    )

    class Meta(object):
        verbose_name = 'Вкладку'
        verbose_name_plural = 'Вкладки'
        ordering = ('id',)

    def __unicode__(self):
        return self.tab_name

class Location(models.Model):
    """
    Место, где размещается контролируемый объект, нампример, комната, дверь, улица и пр.
    """

    name = models.CharField(
        max_length=20,
        default='',
        verbose_name='Расположение',
        help_text='Место, где размещается контролируемый объект',
        blank=False,
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