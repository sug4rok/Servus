# coding=utf-8
from datetime import datetime
from django.db import models

from climate.models import PressureValue
from plugins.arduino.models import Arduino, set_command

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
        db_table = 'climate_sensorbmp_ext'
        verbose_name = 'Датчик BMP'
        verbose_name_plural = 'Датчики BMP085/BMP180'

    def __unicode__(self):
        return self.name

    def set_command(self):
        cmd = 'bmp:%d\n' % self.height_sealevel
        set_command(self, cmd)

    def set_result(self, result):
        if type(result) is str:

            # TODO: Проверка на корректность полученных данных

            press = map(float, result.split(':'))[0]
            press = int(round(press))

            # Добавляем данные датчика в таблицу БД только, если они отличаются от
            # предыдущего показания, иначе обновляем время у предыдущего показания.
            # Это сделано для более быстрой выгрузки данных для графиков, т.к.
            # количество точек существенно сокращается.
            try:
                value = PressureValue.objects.filter(object_id=self.id).latest('id')
            except PressureValue.DoesNotExist:
                value = None
            if value is not None and value.pressure == press:
                value.datetime = datetime.now()
                value.save()
            else:
                PressureValue.objects.create(content_object=self, pressure=press)

                # TODO: Создать функцию событий атм. давления  set_pressure_event(sensor, press)
