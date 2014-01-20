# coding=utf-8
from django.db import models
from django.contrib.sessions.models import Session
from Servus.Servus import SLIDESHOW_ROOT
from Servus.Servus import TAB_APPS

# Getting application type for a new tab
APP_NAME_CHOICES = ((tab_app, tab_app) for tab_app in TAB_APPS) 

IMPORTANCE = (
    (0, 'Простое сообщение'),
    (1, 'Положительное уведомление'),
    (2, 'Информация к сведению'),
    (3, 'Внимание!'),
    (4, 'Опасность!!')
)


# Вкладки и связанные с ними типы приложений
class Tab(models.Model):

    app_name = models.CharField(
        max_length=20,
        choices=APP_NAME_CHOICES,
        verbose_name='Тип приложения',
        help_text='Тип ассоциированного с данной вкладкой приложения Django'
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

    class Meta(object):
        verbose_name = 'Вкладку'
        verbose_name_plural = 'Вкладки'

    def __unicode__(self):
        return self.tab_name


# События, показываемые на Домашней странице (их количество и кретичность также показывается
# на Главной странице. Связь many-to-many с классом RemoteHost необходима, чтобы отделить
# хосты, на которых события уже были просмотрены от "новых" хостов
class Event(models.Model):

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
    )
    event_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время возникновения события'
    )
    session_keys = models.ManyToManyField(
        Session,
        editable=False
    )

    class Meta(object):
        ordering = ('event_datetime',)

    def __unicode__(self):
        return self.event_descr


# Модель для создания в админке триггеров возникновения событий
class EventRule(models.Model):

    event_src = models.ForeignKey(
        Tab,
        verbose_name='Источник события',
    )
    event_descr = models.CharField(
        max_length=255,
        verbose_name='Выводимое сообщение',
        null=True
    )
    event_imp = models.IntegerField(
        max_length=1,
        verbose_name='Критичность',
        choices=IMPORTANCE,
        default=0
    )

    class Meta(object):
        verbose_name = 'Правило'
        verbose_name_plural = 'События'

    def __unicode__(self):
        return self.event_descr


# Время последней модификации папки, содержащей фотоальбомы (static/img/slideshow) -
# тригер при проверке необходимости переиндексации фотоальбомов
class SlideshowChanges(models.Model):

    # Поле для записи время последней модификации папки с фотоальбомами
    mtime = models.FloatField(
        default=0.0
    )


# Абсолютные пути до фотоальбомов, показываемых на Главной странице
class Slideshow(models.Model):

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