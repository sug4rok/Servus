﻿# coding=utf-8
from django.db import models
from django.contrib.auth.models import User


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


class SlideshowChanges(models.Model):
    """
    Время последней модификации папки, содержащей фотоальбомы (static/img/slideshow) -
    тригер при проверке необходимости переиндексации фотоальбомов
    """

    # Поле для записи времени последней модификации папки с фотоальбомами
    mtime = models.FloatField(
        default=0.0
    )


class Slideshow(models.Model):
    """
    Абсолютные пути до фотоальбомов, показываемых на Главной странице
    """

    album_path = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Фотоальбом',
        null=False
    )

    is_shown = models.BooleanField(
        verbose_name='Показывать',
        help_text='Отображение/Исключение фотоальбома из показа на Главной странице',
        default=True
    )

    class Meta(object):
        verbose_name = 'Фотоальбом'
        verbose_name_plural = 'Фотоальбомы в папке slideshow'

    def __unicode__(self):
        return self.album_path