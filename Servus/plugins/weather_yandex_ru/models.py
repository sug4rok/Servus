# coding=utf-8
from datetime import datetime, timedelta

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from weather.utils import WG, file_name_prefix

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
    city_id = models.PositiveIntegerField(
        verbose_name='ID населенного пункта',
        help_text='Пятизначный ID населенного пункта. Узнать ID своего города можно\
        <a href="https://pogoda.yandex.ru/static/cities.xml" target="_blank">здесь</a>',
        unique=True,
        validators=[
            MaxValueValidator(99999),
            MinValueValidator(00000)
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
        return 'http://export.yandex.ru/weather-ng/forecasts/%s.xml' % self.city_id
        
    def __unicode__(self):
        return self.city

    class Meta(object):
        verbose_name = 'прогноз yandex.ru'
        verbose_name_plural = 'Прогнозы погоды от yandex.ru'
        
    class Forecast(WG):
        
        def __init__(self, wp):
            WG.__init__(self, wp)
        
        def parse_to_dict(self):
            weather_data = []

            if self.parsed_xml == -1:
                return weather_data

            def get_wd(wd):
                wds = {'calm': -1, 'n': 0, 'ne': 45, 'nw': 315, 's': 180,
                       'se': 135, 'sw': 225, 'e': 90, 'w': 270}
                return wds[wd]

            def get_file_img(weather_condition, d):
                weather_conditions = {
                    'clear': ['0', 't0d0'],
                    'mostly-clear': ['1', 't0d0'],
                    'mostly-clear-slight-possibility-of-rain': ['1', 't1d0'],
                    'mostly-clear-slight-possibility-of-wet-snow': ['1', 't2d0'],
                    'mostly-clear-slight-possibility-of-snow': ['1', 't3d0'],
                    'partly-cloudy': ['2', 't0d0'],
                    'partly-cloudy-possible-thunderstorms-with-rain': ['2', 't1d0'],
                    'partly-cloudy-and-showers': ['2', 't1d0'],
                    'partly-cloudy-and-light-rain': ['2', 't1d1'],
                    'partly-cloudy-and-rain': ['2', 't1d2'],
                    'partly-cloudy-and-wet-snow-showers': ['2', 't2d0'],
                    'partly-cloudy-and-light-wet-snow': ['2', 't2d1'],
                    'partly-cloudy-and-wet-snow': ['2', 't2d2'],
                    'partly-cloudy-and-snow-showers': ['2', 't3d0'],
                    'partly-cloudy-and-light-snow': ['2', 't3d1'],
                    'partly-cloudy-and-snow': ['2', 't3d2'],
                    'cloudy': ['3', 't0d0'],
                    'cloudy-and-showers': ['3', 't1d0'],
                    'cloudy-and-light-rain': ['3', 't1d1'],
                    'cloudy-and-rain': ['3', 't1d2'],
                    'cloudy-thunderstorms-with-rain': ['3', 't1d5'],
                    'cloudy-and-wet-snow-showers': ['3', 't2d0'],
                    'cloudy-and-light-wet-snow': ['3', 't2d1'],
                    'cloudy-and-wet-snow': ['3', 't2d2'],
                    'cloudy-and-snow-showers': ['3', 't3d0'],
                    'cloudy-and-light-snow': ['3', 't3d1'],
                    'cloudy-and-snow': ['3', 't3d2'],
                    'overcast': ['5', 't0d0'],
                    'overcast-and-showers': ['5', 't1d0'],
                    'overcast-and-light-rain': ['5', 't1d1'],
                    'overcast-and-rain': ['5', 't1d2'],
                    'overcast-thunderstorms-with-rain': ['5', 't1d5'],
                    'overcast-and-wet-snow-showers': ['5', 't2d0'],
                    'overcast-and-light-wet-snow': ['5', 't2d1'],
                    'overcast-and-wet-snow': ['5', 't2d2'],
                    'overcast-and-snow-showers': ['5', 't3d0'],
                    'overcast-and-light-snow': ['5', 't3d1'],
                    'overcast-and-snow': ['5', 't3d2'],
                }
                if weather_condition not in weather_conditions:
                    return [('na', 'na')]
                return [(
                    file_name_prefix(d) + weather_conditions[weather_condition][0],
                    weather_conditions[weather_condition][1]
                )]

            times = {'morning': '07:00', 'day': '13:00', 'evening': '19:00', 'night': '01:00'}
            for day in self.node_value_get('day')[:3]:
                date = day.attributes['date'].value
                for j in xrange(0, 4):
                    weather_condition = self.node_value_get('weather_condition', node=day, subnode_num=j, attr='code')
                    tmp_data = {'wp': self.wp}
                    day_part = self.node_value_get('day_part', node=day, subnode_num=j, attr='type')
                    d = '%s %s' % (date, times[day_part])
                    d_datetime = datetime.strptime(d, self.format)
                    if day_part == 'night':
                        d_datetime += timedelta(days=1)
                    tmp_data['datetime'] = d_datetime
                    tmp_data['temperature'] = self.node_value_get('avg', node=day, subnode_num=j)
                    tmp_data['pressure'] = self.node_value_get('pressure', node=day, subnode_num=j)
                    tmp_data['humidity'] = self.node_value_get('humidity', node=day, subnode_num=j)
                    tmp_data['wind_speed'] = round(
                        float(self.node_value_get('wind_speed', node=day, subnode_num=j)), 0
                    )
                    tmp_data['wind_direction'] = get_wd(
                        self.node_value_get('wind_direction', node=day, subnode_num=j)
                    )
                    for clouds_img, falls_img in get_file_img(weather_condition, tmp_data['datetime']):
                        tmp_data['clouds_img'] = clouds_img
                        tmp_data['falls_img'] = falls_img
                        weather_data.append(tmp_data)
            return weather_data
