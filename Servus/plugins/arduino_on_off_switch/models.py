# coding=utf-8
from django.db import models

from plugins.arduino.models import Arduino, set_command

MODEL = 'OnOffSwitch'


class OnOffSwitch(models.Model):
    """
    Модель переключателей с двумя состояниями (on/off).
    """

    CONTAINER = 'home'
    TYPE = 'OnOffSwitch'
    WIDGET_TYPE = 'positioned'

    name = models.SlugField(
        max_length=20,
        verbose_name='Системное имя',
        unique=True
    )
    controller = models.ForeignKey(
        Arduino,
        verbose_name='Контроллер Arduino',
    )
    controller_pin = models.PositiveSmallIntegerField(
        verbose_name='Вывод (pin) на Arduino',
    )
    state = models.BooleanField(
        default=False,
        editable=False,
    )
    last_changed = models.DateTimeField(
        auto_now=True,
        verbose_name='Время определения состояния',
    )

    class Meta(object):
        db_table = 'home_onoffswitch_ext'
        verbose_name = 'Переключатель'
        verbose_name_plural = 'Переключатели'

    def __unicode__(self):
        return self.name

    def set_command(self):
        cmd = 'sw_state:%d' % self.controller_pin
        set_command(self, cmd)

    def set_result(self, result):

        if result == '0' or result == '1':
            result = bool(int(result))
            if self.state != result:
                self.state = result
                self.save()
