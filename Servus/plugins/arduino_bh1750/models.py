# coding=utf-8
from datetime import datetime
from django.db import models

from climate.models import AmbientLightValue
from plugins.arduino.models import Arduino, set_command

MODEL = 'SensorBH1750'


class SensorBH1750(models.Model):
    """
    Модель датчиков атмосферного давления BMP085/BMP180 (GY-68).
    """

    CONTAINER = 'climate'
    TYPE = 'AmbientLightSensor'
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

    class Meta(object):
        verbose_name = 'Датчик BH1750'
        verbose_name_plural = 'Датчики BH1750'

    def __unicode__(self):
        return self.name

    def set_command(self):
        cmd = 'bh1750:\n'
        set_command(self, cmd)

    def set_result(self, result):
        if type(result) is str and result.isdigit():
            light = int(result)

            # Добавляем данные датчика в таблицу БД только, если они отличаются от
            # предыдущего показания, иначе обновляем время у предыдущего показания.
            # Это сделано для более быстрой выгрузки данных для графиков, т.к.
            # количество точек существенно сокращается.
            try:
                value = AmbientLightValue.objects.filter(object_id=self.id).latest('id')
            except AmbientLightValue.DoesNotExist:
                value = None
            if value is not None and value.ambient_light == light:
                value.datetime = datetime.now()
                value.save()
            else:
                AmbientLightValue.objects.create(content_object=self, ambient_light=light)
