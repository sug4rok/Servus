# coding=utf-8
import time
from django.db import models

from climate.models import TempHumidValue
from plugins.arduino.models import Arduino
from .utils import check_dht_data, set_climate_event

MODEL = 'SensorDHT'

DHT_TYPES = (
    ('dht11', 'DHT11'),
    ('dht21', 'DHT21'),
    ('dht22', 'DHT22'),
)

LOCATION_TYPES = (
    ('inside', 'В помещении'),
    ('outside', 'На улице'),
    ('other', 'Другое'),
)


class SensorDHT(models.Model):
    """
    Модель для добавления новых датчиков влажности и температуры DHT
    (DHT11, DHT21 и DHT22).
    """

    CONTAINER = 'climate'
    TYPE = 'TempHumidSensor'
    WIDGET_TYPE = 'positioned'

    name = models.SlugField(
        max_length=20,
        verbose_name='Системное имя',
        unique=True
    )
    type = models.SlugField(
        choices=DHT_TYPES,
        default='dht11',
        verbose_name='Тип датчика',
    )
    controller = models.ForeignKey(
        Arduino,
        verbose_name='Контроллер Arduino',
    )
    controller_pin = models.PositiveSmallIntegerField(
        verbose_name='Вывод (pin) на Arduino',
        unique=False,
    )
    location_type = models.SlugField(
        choices=LOCATION_TYPES,
        default='inside',
        verbose_name='Тип расположение датчика',
    )

    class Meta(object):
        verbose_name = 'Датчик DHT'
        verbose_name_plural = 'Датчики DHT'

    def __unicode__(self):
        return self.name

    def get_data(self):
        cmd = '%s:%d\n' % (self.type, self.controller_pin)

        controller = self.controller.Command(self)

        if controller.state[0]:
            counter = 3
            while counter:
                result = controller.send(cmd)

                if controller.state[0]:
                    try:
                        humid, temp = map(float, result.split(':'))

                        # Проверяем полученные данные на возможные ошибки показаний.
                        # Делаем три измерения подряд с 5 секундной паузой, чтобы удостоверится, что
                        # "запредельные" значения - это не ошибка датчика
                        if check_dht_data(temp, humid, self.type):
                            counter -= 1
                            time.sleep(2)
                        else:
                            TempHumidValue.objects.create(content_object=self,
                                                          temperature=round(temp, 0),
                                                          humidity=round(humid, 0))
                            set_climate_event(self, humid, temp)
                            break
                    except ValueError:
                        counter -= 1
                        time.sleep(2)
                else:
                    break

            controller.close_port()
