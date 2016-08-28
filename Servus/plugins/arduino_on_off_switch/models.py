# coding=utf-8
from datetime import datetime
import logging

from django.db import models

from plugins.arduino.models import Arduino

logger = logging.getLogger(__name__)

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
        verbose_name = 'Переключатель'
        verbose_name_plural = 'Переключатели'

    def __unicode__(self):
        return self.name

    def get_data(self):
        cmd = 'sw_state:%d\n' % self.controller_pin

        controller = self.controller.Command(self)

        if controller.state[0]:
            result = controller.send(cmd)

            try:
                result = int(result)
                if controller.state[0] and (result == 0 or result == 1):
                    result = bool(result)
                    if self.state != result:
                        self.state = result
                        self.save()
            except ValueError:
                logger.error(u'OnOffSwitch: Ошибка получения данных от %s', self.name)

            controller.close_port()
