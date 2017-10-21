# coding=utf-8
from django.db import models
from events.utils import event_setter

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

    def set_result(self, result):
        if result is not None:
            try:
                self.temperature = result
                self.set_event(result)
            except ValueError:
                pass

    def set_event(self, temp):
        """
        Запись в журнал событий данных, находящихся за пределами нормы.
        :param temp: int Значение температуры
        """
        
        if temp <= 20 or temp >= 50:
            msg = u'Температура HDD вышла из безопасного диапазона ({0}°C)'.format(temp)
            event_setter('system', msg, 4, email=True)
            self.level = 4
        elif temp <= 25 or temp >= 45:
            msg = u'Температура HDD близка к критичной ({0}°C)'.format(temp)
            event_setter('system', msg, 3)
            self.level = 3
        else:
            self.level = 2

        self.save()
        