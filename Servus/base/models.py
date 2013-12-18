# coding=utf-8
from django.db import models
from django.contrib.sessions.models import Session
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
    # Поле для отметки факта изменений в админке в разделе "Исключаемые фотоальбомы"
    was_excluded = models.BooleanField(
        default=False
    )


# Абсолютные пути до фотоальбомов, показываемых на Главной странице
class Slideshow(models.Model):

    album_path = models.ImageField(
        upload_to='.'
    )

    def __unicode__(self):
        return 'Slideshow class'


def set_was_excluded():
    try:
        obj_ssch = SlideshowChanges.objects.get(id=1)
        obj_ssch.was_excluded = True
        obj_ssch.save()
    except SlideshowChanges.DoesNotExist:
        pass


# Список фотоальбомов, исключаемых из показа на главной странице
class SlideshowExclude(models.Model):

    album_exclude = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Фотоальбом',
        help_text='Название папки с фотографиями или подпапками, которые необходимо исключить \
            из показа на Главной странице.',
        null=False
    )

    class Meta(object):
        verbose_name = 'Исключения'
        verbose_name_plural = 'Исключаемые фотоальбомы'

    # Добавим к методу save() возможность менять состояние триггера was_excluded
    # в таблице SlideshowChanges для указания, что нужно переиндексировать
    # все фотоальбомы и добавить/исключить те из них, что были удалены/созданы
    # при помощи данной модели.
    def save(self):
        set_was_excluded()
        super(SlideshowExclude, self).save()

    # Аналогично методу save(), но этот метод не работает в админке на 2013.12.09
    # (Django 1.6)
    def delete(self):
        set_was_excluded()
        super(SlideshowExclude, self).delete()

    def __unicode__(self):
        return self.album_exclude