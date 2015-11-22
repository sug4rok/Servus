# coding=utf-8
from django.db import models

MODEL = 'PingHost'


class PingHost(models.Model):
    """
    Модель для хранения информации о сетевых устройствах и их доступности
    в сети.
    """

    CONTAINER = 'system'
    TYPE = 'Ping'
    WIDGET_TYPE = 'tiled'

    name = models.CharField(
        max_length=50,
        verbose_name='Имя/название хоста',
        unique=False
    )
    ip_address = models.GenericIPAddressField(
        default='0.0.0.0',
        verbose_name='IP-адрес',
        protocol='IPv4',
    )
    online = models.BooleanField(
        default=False,
        editable=False,
    )
    last_changed = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время последней смены статуса'
    )

    class Meta(object):
        verbose_name = 'хост'
        verbose_name_plural = 'Сетевые устройства'

    def __unicode__(self):
        return self.ip_address
