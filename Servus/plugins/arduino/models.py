# coding=utf-8
from django.db import models

MODEL = 'Arduino'

class Arduino(models.Model):
    """
    Модель для описания подключенного контроллера Arduino
    """
    
    CONTAINER = 'system'
    ADMIN = True
    
    name = models.CharField(
        max_length=50,
        verbose_name='Модель',
        unique=True
    )
    port = models.CharField(
        default=1,
        max_length=10,
        verbose_name='COM-порт',
        help_text='COM-порт, к которому подключен контроллер.<br>\
                  Например:<br>\
                  В Windows порт = № порта - 1;<br>\
                  В Linux   порт = ttyACM0'
    )
    
    class Meta(object):
        verbose_name = 'Контроллер Arduino'
        verbose_name_plural = 'Контроллеры Arduino'

    def __unicode__(self):
        return '%s: %s' % (self.name, self.port)