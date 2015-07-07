# coding=utf-8
from django.db import models
from django.contrib.sessions.models import Session


class Event(models.Model):
    """
    События, показываемые на Домашней странице (их количество и кретичность также показывается
    на Главной странице. Связь many-to-many с классом Session необходима, чтобы отделить
    хосты, на которых события уже были просмотрены от "новых" хостов
    """

    source = models.SlugField(
        max_length=20,
        verbose_name='Источник события',
    )
    message = models.CharField(
        max_length=255,
        verbose_name='Сообщение',
        null=True
    )
    level = models.PositiveSmallIntegerField(
        verbose_name='Критичность',
        default=2,
    )
    datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время возникновения события'
    )
    session_keys = models.ManyToManyField(
        Session,
        editable=False
    )
    email_sent = models.BooleanField(
        default=False
    )
    sms_sent = models.BooleanField(
        default=False
    )

    class Meta(object):
        ordering = ('datetime',)

    def __unicode__(self):
        return u'%s: %s' % (self.source, self.message)
