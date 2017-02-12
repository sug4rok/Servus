# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

MODEL = 'SMSRu'


class SMSRu(models.Model):
    """
    Модель для настройки отправки сообщений через сайт sms.ru
    """

    CONTAINER = 'system'
    TYPE = 'SMS'

    name = models.ForeignKey(
        User,
        verbose_name='Пользователь',
    )
    phone = models.BigIntegerField(
        verbose_name='Номер телефона',
        help_text='Номер телефона для отправки сообщений через сервис sms.ru.<br>\
            Диапазон номеров ограничен 1*e10 - 9,(9)*e12 (подробности на sms.ru).<br>\
            Формат для РФ 7xxxyyyyyyy, где xxx - код оператора, yyyyyyy - номер телефона.<br>',
        validators=[
            MaxValueValidator(9999999999999),
            MinValueValidator(10000000000)
        ]
    )
    sms_ru_id = models.CharField(
        max_length=40,
        verbose_name='sms.ru api_id',
        blank=True,
        null=True
    )

    class Meta(object):
        db_table = 'system_smsru_ext'
        verbose_name = 'sms.ru id'
        verbose_name_plural = 'sms.ru id'

    def __unicode__(self):
        return '%s: %s' % (self.name.username, self.sms_ru_id)
