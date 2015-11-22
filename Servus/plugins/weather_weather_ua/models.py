# coding=utf-8
from datetime import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from weather.utils import WG, file_name_prefix

MODEL = 'WeatherUa'


class WeatherUa(models.Model):
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
    city_id = models.PositiveIntegerField(
        verbose_name='ID населенного пункта',
        help_text='Узнать ID своего города можно поиском по базе городов,\
        например, так: http://xml.weather.ua/1.2/city/?search=<font color="#5577cc">Санкт-Петербург</font>',
        unique=True,
        validators=[
            MaxValueValidator(99999),
            MinValueValidator(0)
        ]
    )
    on_sidebar = models.BooleanField(
        default=False,
        verbose_name='Участвует в усреднении',
        help_text='Отметьте, если данный прогноз должен учитываться при расчете усредненной оценки \
            прогноза погоды в виде виджета на Главной странице.<br>\
           (Отмечать, по понятным причинам, имеет смысл прогнозы для одного и того же города)'
    )

    def get_url(self):
        return 'http://xml.weather.ua/1.2/forecast/%s?dayf=4?lang=ru' % self.city_id

    def __unicode__(self):
        return self.city

    class Meta(object):
        verbose_name = 'прогноз weather.ua'
        verbose_name_plural = 'Прогнозы погоды от weather.ua'

    class Forecast(WG):

        def __init__(self, wp):
            WG.__init__(self, wp)

        def parse_to_dict(self):
            weather_data = []

            if self.parsed_xml == -1:
                return weather_data

            def get_clouds_img(clouds, d):
                clouds_ranges = [
                    xrange(0, 5),
                    xrange(5, 10),
                    xrange(10, 20),
                    xrange(20, 25),
                    xrange(25, 30),
                    xrange(30, 101),
                ]
                for num, clouds_range in enumerate(clouds_ranges):
                    if clouds in clouds_range:
                        return file_name_prefix(d) + str(num)
                return 'na'

            def get_falls_img(clouds):
                falls_ranges = {
                    't0d0': xrange(0, 40),
                    't1d0': xrange(40, 50),
                    't1d1': xrange(50, 52),
                    't1d2': xrange(52, 55),
                    't1d3': xrange(55, 58),
                    't1d4': xrange(58, 60),
                    't1d5': xrange(60, 70),
                    't1d6': xrange(70, 80),
                    't2d0': xrange(80, 82),
                    't2d1': xrange(82, 84),
                    't2d2': xrange(84, 86),
                    't2d3': xrange(86, 88),
                    't2d4': xrange(88, 90),
                    't3d0': xrange(90, 92),
                    't3d1': xrange(92, 94),
                    't3d2': xrange(94, 96),
                    't3d3': xrange(96, 98),
                    't3d4': xrange(98, 100),
                }
                for r in falls_ranges:
                    if clouds in falls_ranges[r]:
                        return r
                return 'na'

            for day in self.node_value_get('day')[:9]:
                clouds = int(self.node_value_get('cloud', node=day, subnode_num=0))
                tmp_data = {'wp': self.wp}
                d = '%s %s:00' % (day.attributes['date'].value, day.attributes['hour'].value)
                tmp_data['datetime'] = datetime.strptime(d, self.format)
                tmp_data['temperature'] = int(
                    self.node_value_get('min', node=self.node_value_get('t', node=day)[0], subnode_num=0)
                ) + 1
                tmp_data['pressure'] = int(
                    self.node_value_get('min', node=self.node_value_get('p', node=day)[0], subnode_num=0)
                ) + 1
                tmp_data['humidity'] = int(
                    self.node_value_get('min', node=self.node_value_get('hmid', node=day)[0], subnode_num=0)
                ) + 1
                tmp_data['wind_speed'] = int(
                    self.node_value_get('min', node=self.node_value_get('wind', node=day)[0], subnode_num=0)
                ) + 1
                tmp_data['wind_direction'] = self.node_value_get(
                    'rumb', node=self.node_value_get('wind', node=day)[0], subnode_num=0
                )
                tmp_data['clouds_img'] = get_clouds_img(clouds, tmp_data['datetime'])
                tmp_data['falls_img'] = get_falls_img(clouds)
                weather_data.append(tmp_data)

            return weather_data
