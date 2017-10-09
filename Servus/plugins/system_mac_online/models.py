# coding=utf-8
from django.db import models
from base.models import MACAddressField

MODEL = 'MACAddress'


class MACAddress(models.Model):
    """ Модель для хранения состояния MAC-адресов хостов в сети. """

    CONTAINER = 'system'
    TYPE = 'AtHome'
    WIDGET_TYPE = 'tiled'

    name = models.CharField(
        max_length=50,
        verbose_name='Имя/название устройства',
        unique=False
    )
    mac = MACAddressField(
        verbose_name='MAC-адрес устройства',
        help_text='MAC-адрес любого носимого устройства (телефон, часы и пр.), <br>\
            подключенного к той же сети, что и сервер. Формат: 11:22:33:aa:bb:cc',
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
        db_table = 'system_macaddress_ext'
        verbose_name = 'MAC-адрес'
        verbose_name_plural = 'MAC-адреса устройств'

    def __unicode__(self):
        return self.mac

    def save(self, *args, **kwargs):
        self.mac = self.mac.replace('-', ':').lower()
        super(MACAddress, self).save(*args, **kwargs)
