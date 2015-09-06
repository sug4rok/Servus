# coding=utf-8
from django.db import models

MODEL = 'YandexRU'


class YandexRU(models.Model):
    """
    Модель для храннения ссылок API для выбранных населенных пунктов
    """
    
    CONTAINER = 'weather'
    TYPE = 'Forecast'

    city = models.CharField(
        max_length=20,
        verbose_name='Населенный пункт',
        help_text='Название населенного пункта, для которого отображается прогноз погоды.',
    )
    url = models.URLField(
        verbose_name='URL на XML-API',
        help_text='url на XML-API прогноза погоды от yandex.ru вида:<br>\
            <strong>http://export.yandex.ru/weather-ng/forecasts/<font color="#5577cc">XXXX</font>.xml</strong><br><br>\
            ,где <strong><font color="#5577cc">XXXX</font></strong> - код населенного пункта прогноза погоды.\
            Например, для Санкт-Петербурга (Россия) код <strong><font color="#5577cc">26063</font></strong>',
        unique=True
    )
    on_sidebar = models.BooleanField(
        default=False,
        verbose_name='Участвует в усреднении',
        help_text='Отметьте, если данный прогноз должен учитываться при расчете усредненной оценки \
            прогноза погоды в виде виджета на Главной странице.<br>\
           (Отмечать, по понятным причинам, имеет смысл прогнозы для одного и того же города)'
    )

    class Meta(object):
        verbose_name = 'прогноз yandex.ru'
        verbose_name_plural = 'Прогнозы погоды от yandex.ru'

    def __unicode__(self):
        return 'yandex.ru forecast class'
