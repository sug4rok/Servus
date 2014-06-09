# coding=utf-8
from django.db import models
from django.contrib.sessions.models import Session


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
    event_imp = models.PositiveSmallIntegerField(
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