# coding=utf-8
from django.db import models

from climate.models import PressureValue
from plugins.arduino.models import Arduino

MODEL = 'SensorBMP'


class SensorBMP(models.Model):
    """
    Модель датчиков атмосферного давления BMP085/BMP180 (GY-68).
    """

    CONTAINER = 'climate'
    TYPE = 'PressureSensor'
    WIDGET_TYPE = 'positioned'

    name = models.SlugField(
        max_length=10,
        verbose_name='Системное имя',
        unique=True
    )
    controller = models.ForeignKey(
        Arduino,
        verbose_name='Контроллер Arduino',
    )
    height_sealevel = models.DecimalField(
        default=0,
        max_digits=5,
        decimal_places=1,
        verbose_name='Высота над уровнем моря',
    )

    class Meta(object):
        verbose_name = 'Датчик BMP'
        verbose_name_plural = 'Датчики BMP085/BMP180'

    def __unicode__(self):
        return self.name

    def get_data(self):
        cmd = 'bmp:%d\n' % self.height_sealevel

        controller = self.controller.Command(self)

        if controller.state[0]:
            result = controller.send(cmd)
            # TODO: Проверка на корректность полученных данных
            if controller.state[0]:
                press = map(float, result.split(':'))[0]

                PressureValue.objects.create(content_object=self, pressure=round(press, 0))
                # TODO: Создать функцию событий атм. давления  set_pressure_event(sensor, press)

            controller.close_port()