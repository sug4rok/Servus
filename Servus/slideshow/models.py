# coding=utf-8
from django.db import models


class SlideshowChanges(models.Model):
    """
    Время последней модификации папки, содержащей фотоальбомы (media/slideshow) -
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
