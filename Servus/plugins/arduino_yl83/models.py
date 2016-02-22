# coding=utf-8
from django.db import models

from climate.models import RaindropValue
from plugins.arduino.models import Arduino

MODEL = 'SensorYL83'


class SensorYL83(models.Model):
    """
    Модель датчиков дождя YL-83.
    """

    CONTAINER = 'climate'
    TYPE = 'RaindropSensor'
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
        unique=False,
    )

    class Meta(object):
        verbose_name = 'Датчик YL-83'
        verbose_name_plural = 'Датчики YL-83'

    def __unicode__(self):
        return self.name

    def get_data(self):
        cmd = 'rain:%d\n' % self.controller_pin

        controller = self.controller.Command(self)

        if controller.state[0]:
            result = controller.send(cmd)

            # TODO: Проверка на корректность полученных данных
            if controller.state[0]:
                RaindropValue.objects.create(content_object=self, raindrop=int(result))

            controller.close_port()
