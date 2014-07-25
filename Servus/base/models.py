# coding=utf-8
from django.db import models


class UserProfile(models.Model):
    """
    Пользователи, которым будут приходить уведомления
    """

    name = models.CharField(
        max_length=36,
        verbose_name='Имя',
    )
    email = models.EmailField(
        verbose_name='E-mail',
        blank=True,
        null=True
    )
    phone = models.PositiveIntegerField(
        max_length=11,
        verbose_name='Номер телефона',
        help_text='Номер в формате 7xxxyyyyyyy, где xxx - код оператора, yyyyyyy - номер телефона.<br>\
            Номер телефона нужен для отправки сообщений через сервис sms.ru.',
        blank=True,
        null=True
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

    app_name = models.CharField(
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

    def __unicode__(self):
        return self.tab_name