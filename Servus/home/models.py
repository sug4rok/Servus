# coding=utf-8
from django.db import models


class Plan(models.Model):
    """
    Модель для добавления на главную страницу планировки помещений
    """

    image = models.ImageField(
        upload_to='plans',
        verbose_name='Файл с планировкой',
        help_text='Выберите файл с планировкой помещения',
    )
    description = models.CharField(
        max_length=20,
        verbose_name='Название',
    )
    is_shown = models.BooleanField(
        verbose_name='Показана',
        help_text='Отображение/Скрытие планировки помещения (необходим перезапуск web-сервера)',
        default=True
    )

    class Meta(object):
        verbose_name = 'Планировку'
        verbose_name_plural = 'Планировки помещения'

    def __unicode__(self):
        return self.description
