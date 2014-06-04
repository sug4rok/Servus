# coding=utf-8
from django.db import models


class WeatherProvider(models.Model):
    """
    Модель для хранения данных о провайдерах прогнозов погоды и выбранных населенных пунктах
    """

    weather_provider = models.CharField(
        max_length=20,
        choices=(
            # ('rp5', 'rp5.ru'), # С 1 июля 2014 недоступен бесплатно
            ('wua', 'weather.ua'),
            ('ya', 'Яндекс.Погода'),
            ('owm', 'Open Weather Map')
        ),
        verbose_name='Прогнозный сайт',
        help_text='Сайт, предоставляющий API прогноза погоды.'
    )
    weather_url = models.URLField(
        verbose_name='URL на XML-API',
        # url для rp5.ru: http://rp5.ru/xml/7285/00000/ru
        help_text='url на XML-API сайта прогноза погоды. Для выбранного прогнозного сайта\
            впишите соответствующий URL<br><br>\
            - weather.ua: <strong>http://xml.weather.co.ua/1.2/forecast/<font color="#5577cc">XXXX</font>?dayf=4?lang=ru</strong><br>\
            - Яндекс.Погода: <strong>http://export.yandex.ru/weather-ng/forecasts/<font color="#5577cc">XXXX</font>.xml</strong><br>\
            - Open Weather Map: <strong>http://api.openweathermap.org/data/2.5/forecast/daily?q=<font color="#5577cc">XXXX</font>&mode=xml&units=metric&cnt=4</strong><br><br>\
            ,где <strong><font color="#5577cc">XXXX</font></strong> - код города, для которого составляется прогноз погоды. \
            Например, для Санкт-Петербурга (Россия) коды будут следующие:<br><br>\
            - weather.ua: <strong><font color="#5577cc">773</font></strong><br>\
            - Яндекс.Погода: <strong><font color="#5577cc">26063</font></strong><br>\
            - Open Weather Map: <strong><font color="#5577cc">St.Petersburg</font></strong>',
        unique=True
    )
    weather_city = models.CharField(
        max_length=20,
        verbose_name='Населенный пункт',
        help_text='Название города, для которого отображается прогноз погоды \
            (необязательное поле, необходимо только для отличия на странице двух прогонозов \
            погоды одного и того же провайдера).',

        blank=True,
        null=True
    )
    on_sidebar = models.BooleanField(
        default=False,
        verbose_name='Участвует в усреднении',
        help_text='Отметьте, если данный прогноз должен учитываться при расчете усредненной оценки прогноза погоды на панели слева.<br>\
            (Отмечать, по понятным причинам, имеет смысл прогнозы для одного и того же города)'
    )

    class Meta(object):
        verbose_name = 'Прогноз погоды'
        verbose_name_plural = 'Прогноз погоды'

    def __unicode__(self):
        return 'Forecast class for %s weather provider' % self.weather_provider


class Weather(models.Model):
    """
    Модель для хранения погодных данных
    """

    wp = models.ForeignKey(
        WeatherProvider
    )
    datetime = models.DateTimeField(
        verbose_name='Время прогноза',
        default='2013-08-30 00:00'
    )
    clouds = models.PositiveSmallIntegerField(
        max_length=2,
        verbose_name='Облачность',
        default=0
    )
    precipitation = models.FloatField(
        max_length=4,
        verbose_name='Осадки',
        default=0.0
    )
    temperature = models.SmallIntegerField(
        max_length=3,
        verbose_name='Температура',
        default=0
    )
    pressure = models.PositiveSmallIntegerField(
        max_length=3,
        verbose_name='Давление',
        default=0
    )
    humidity = models.PositiveSmallIntegerField(
        max_length=2,
        verbose_name='Влажность',
        default=0
    )
    wind_speed = models.PositiveSmallIntegerField(
        max_length=2,
        verbose_name='Ветер',
        default=0
    )
    wind_direction = models.SmallIntegerField(
        max_length=3,
        verbose_name='Направление ветра',
        default=0
    )
    clouds_img = models.CharField(
        max_length=3,
        default='na'
    )
    falls_img = models.CharField(
        max_length=4,
        default='na'
    )

    def __unicode__(self):
        return 'Forecast class for %s weather provider' % self.wp_id

    class Meta(object):
        ordering = ('wp',)