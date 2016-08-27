# coding=utf-8
from django.db import models

from plugins.arduino_on_off_switch.models import OnOffSwitch

MODEL = 'ReedSwitch'

LOCATION_TYPES = (
    ('door', 'Дверь'),
    ('window', 'Окно')
)


class ReedSwitch(OnOffSwitch):
    """
    Модель для герконов.
    """

    location_type = models.SlugField(
        choices=LOCATION_TYPES,
        default='door',
        verbose_name='Объект',
    )

    class Meta(object):
        verbose_name = 'Геркон'
        verbose_name_plural = 'Герконы'
