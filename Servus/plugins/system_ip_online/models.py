# coding=utf-8
from django.db import models

MODEL = 'IPAddress'


class IPAddress(models.Model):
    """
    Модель для хранения информации о сетевых устройствах и их доступности
    в сети.
    """

    CONTAINER = 'system'
    TYPE = 'Ping'
    WIDGET_TYPE = 'tiled'

    name = models.CharField(
        max_length=50,
        verbose_name='Имя/название устройства',
        unique=False,
    )
    ip_address = models.GenericIPAddressField(
        default='0.0.0.0',
        verbose_name='IP-адрес',
        protocol='IPv4',
        unique=True,
    )
    online = models.BooleanField(
        default=False,
        editable=False,
    )
    last_changed = models.DateTimeField(
        auto_now=True,
        verbose_name='Время последней смены статуса'
    )

    class Meta(object):
        db_table = 'system_ipaddress_ext'
        verbose_name = 'IP-адрес'
        verbose_name_plural = 'IP-адреса устройств'

    def __unicode__(self):
        return self.ip_address
