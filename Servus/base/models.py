# coding=utf-8
from django.db import models
from django.contrib.sessions.models import Session
from Servus.Servus import SLIDESHOW_ROOT


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


class Event(models.Model):
    """
    События, показываемые на Домашней странице (их количество и кретичность также показывается
    на Главной странице. Связь many-to-many с классом Session необходима, чтобы отделить
    хосты, на которых события уже были просмотрены от "новых" хостов
    """

    event_src = models.CharField(
        max_length=20,
        verbose_name='Источник события',
    )
    event_descr = models.CharField(
        max_length=255,
        verbose_name='Описание события',
        null=True
    )
    event_imp = models.IntegerField(
        max_length=1,
        verbose_name='Критичность',
        default=2,
    )
    event_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время возникновения события'
    )
    session_keys = models.ManyToManyField(
        Session,
        editable=False
    )
    was_sent = models.BooleanField(
        default=False
    )

    class Meta(object):
        ordering = ('event_datetime',)

    def __unicode__(self):
        return self.event_descr


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
        verbose_name_plural = 'Фотоальбомы в %s' % SLIDESHOW_ROOT

    def __unicode__(self):
        album_path = self.album_path.replace('%s/' % SLIDESHOW_ROOT, '')
        if album_path == SLIDESHOW_ROOT:
            return '/'
        else:
            return album_path