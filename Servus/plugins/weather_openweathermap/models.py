# coding=utf-8
from datetime import datetime, timedelta

from django.db import models

from weather.utils import WG, file_name_prefix

MODEL = 'OpenWeatherMap'


class OpenWeatherMap(models.Model):
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
        help_text='url на XML-API прогноза погоды от openweathermap.org вида:<br>\
            <strong>http://api.openweathermap.org/data/2.5/forecast/daily?q=\
            <font color="#5577cc">XXXX</font>&mode=xml&units=metric&cnt=4&appid=\
            <font color="#5577cc">YYYY</font></strong><br><br>\
            ,где <strong><font color="#5577cc">XXXX</font></strong> - код населенного пункта\
            прогноза погоды,<br><strong><font color="#5577cc">YYYY</font></strong> - Ваш ключ\
            API (с 9 октября требуется регистрация).<br>Например, для Санкт-Петербурга (Россия)\
            код <strong><font color="#5577cc">St.Petersburg</font></strong>',
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
        verbose_name = 'прогноз openweathermap.org'
        verbose_name_plural = 'Прогнозы погоды от openweathermap.org'

    class Forecast(WG):
        def parse_to_dict(self):
            weather_data = []

            if self.parsed_xml == -1:
                return weather_data

            def get_clouds_img(clouds, d):
                clouds_ranges = {
                    '800': '0',
                    '801': '1',
                    '802': '2',
                    '803': '3',
                    '804': '5',
                }
                if clouds in clouds_ranges:
                    return file_name_prefix(d) + clouds_ranges[clouds]
                return file_name_prefix(d) + '5'

            def get_falls_img(clouds):
                falls_ranges = {
                    't1d0': ['321', '520', '521', '522'],
                    't1d1': ['200', '300', '310', '500'],
                    't1d2': ['201', '301', '311', '501'],
                    't1d3': ['202', '302', '312', '502'],
                    't1d4': ['210', '230', '503', '504'],
                    't1d5': ['211', '212', '221', '231', '232'],
                    't1d6': ['906'],
                    't2d2': ['511', '611'],
                    't3d0': ['621'],
                    't3d2': ['600'],
                    't3d3': ['601'],
                    't3d4': ['602']
                }
                for r in falls_ranges:
                    if clouds in falls_ranges[r]:
                        return r
                return 't0d0'

            times = [('morn', '07:00'), ('day', '13:00'), ('eve', '19:00'), ('night', '01:00')]
            for day in self.node_value_get('time')[:3]:
                for day_part, time in times:
                    tmp_data = {'wp': self.wp}
                    d = '%s %s' % (day.attributes['day'].value, time)
                    d_datetime = datetime.strptime(d, self.format)
                    if day_part == 'night':
                        d_datetime += timedelta(days=1)
                    tmp_data['datetime'] = d_datetime
                    tmp_data['clouds'] = self.node_value_get('clouds', node=day, subnode_num=0, attr='all')
                    precipitation = self.node_value_get('precipitation', node=day, subnode_num=0, attr='value')
                    if precipitation != -1:
                        tmp_data['precipitation'] = precipitation
                    tmp_data['temperature'] = round(
                        float(self.node_value_get('temperature', node=day, subnode_num=0, attr=day_part)), 0
                    )
                    tmp_data['pressure'] = round(
                        float(self.node_value_get('pressure', node=day, subnode_num=0, attr='value')) / 1.333224, 0
                    )
                    tmp_data['humidity'] = self.node_value_get('humidity', node=day, subnode_num=0, attr='value')
                    tmp_data['wind_speed'] = round(
                        float(self.node_value_get('windSpeed', node=day, subnode_num=0, attr='mps')), 0
                    )
                    tmp_data['wind_direction'] = self.node_value_get('windDirection', node=day, subnode_num=0,
                                                                     attr='deg')
                    symbol_num = self.node_value_get('symbol', node=day, subnode_num=0, attr='number')
                    tmp_data['clouds_img'] = get_clouds_img(symbol_num, tmp_data['datetime'])
                    tmp_data['falls_img'] = get_falls_img(symbol_num)
                    weather_data.append(tmp_data)

            return weather_data
