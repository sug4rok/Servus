# coding=utf-8
from datetime import datetime
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
    # Максимальное и минимальное значения показаний датчика. В идеальных условиях равны соответсвенно 1023 и 0.
    # Ставим соотвественно изначально 0 и 1023 для для дальнейшей cамонастройки.
    max_value = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='max значение',
    )
    min_value = models.PositiveSmallIntegerField(
        default=1023,
        verbose_name='min значение',
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
                raindrop = int(result)
            
                # Добавляем данные датчика в таблицу БД только, если они отличаются от
                # предыдущего показания, иначе обновляем время у предыдущего показания.
                # Это сделано для более быстрой выгрузки данных для графиков, т.к.
                # количество точек существенно сокращается.
                try:
                    value = RaindropValue.objects.filter(object_id=self.id).latest('id')
                except RaindropValue.DoesNotExist:
                    value = None
                if value is not None and value.raindrop == raindrop:
                    value.datetime=datetime.now()
                    value.save()
                else:
                    RaindropValue.objects.create(content_object=self, raindrop=raindrop)
                    
                    # Самонастройка крайних диапазонов измерений датчика.
                    if raindrop < self.min_value:
                        self.min_value = raindrop
                        self.save()
                    if raindrop > self.max_value:
                        self.max_value = raindrop
                        self.save()

            controller.close_port()
