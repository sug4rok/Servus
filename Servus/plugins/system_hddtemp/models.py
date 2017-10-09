# coding=utf-8
from django.db import models

MODEL = 'HDDTemp'

HDD_TYPE = (
    (None, '?'),
    ('SATA', 'SATA'),
    ('PATA', 'PATA'),
    ('SCSI', 'SCSI'),
)


class HDDTemp(models.Model):
    """
    Модель переключателей с двумя состояниями (on/off).
    """

    CONTAINER = 'system'
    TYPE = 'BoardSensors'
    WIDGET_TYPE = 'positioned'

    name = models.SlugField(
        max_length=5,
        verbose_name='Диск (без полного пути)',
        default='sda',
        unique=True
    )
    type = models.SlugField(
        choices=HDD_TYPE,
        default='SATA',
        verbose_name='Тип HDD',
    )
    temperature = models.SmallIntegerField(
        default=0,
        editable=False,
    )
    last_changed = models.DateTimeField(
        auto_now=True,
        verbose_name='Время определения состояния',
    )

    class Meta(object):
        db_table = 'system_hddtemp_ext'
        verbose_name = 'Жесткий диск'
        verbose_name_plural = 'Жесткие диски'

    def __unicode__(self):
        return '/dev/' + self.name
