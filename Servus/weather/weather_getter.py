# coding=utf-8
from xml.dom import minidom
from urllib2 import urlopen, HTTPError
from datetime import datetime, timedelta
from events.utils import event_setter


class WG(object):
    """
    Класс, реализующий доставку прогноза погоды с XML-API прогнозных сайтов в таблицу weather_weather
    базы данных. Функция parse_to_dict реализуется в каждом классе-потомке отдельно, т.к. 
    у каждого прогнозного сайта свой API и парсинг XML-данных уникален.
    """

    def __init__(self, wp):
        self.wp = wp
        self.wp_url = wp.weather_url        
        self.parsed_xml = self.parse_xml()
        self.format = '%Y-%m-%d %H:%M'

    def parse_xml(self):
        try:
            url_sock = urlopen(self.wp_url)
        except HTTPError, err:
            event_setter('system', u'Weather %s: urllib2 HTTPError: %s' % (self.wp.weather_provider, err.code),
                         3, delay=3, sms=False)
            return -1
        try:
            parsed_xml = minidom.parse(url_sock)
            return parsed_xml
        except:
            event_setter('system', u'Weather: Ошибка парсинга для %s' % self.wp.weather_provider, 3, delay=3, sms=False)
            return -1
        finally:
            url_sock.close()

    def node_value_get(self, tag, node=None, subnode_num=None, attr=None):
        if node is not None:
            subnodes = node.getElementsByTagName(tag)
        else:
            subnodes = self.parsed_xml.getElementsByTagName(tag)
        if subnode_num is not None:
            if attr is not None:
                try:
                    return subnodes[subnode_num].attributes[attr].value
                except KeyError:
                    return -1
            else:
                return subnodes[subnode_num].childNodes[0].nodeValue
        else:
            return subnodes
        
    @staticmethod
    def file_name_prefix(d):
        hours_format = '%H'
        h = int(d.strftime(hours_format))
        if 8 < h <= 20:
            prefix = 'cd'
        else:
            prefix = 'cn'         
        return prefix 
    
    def __str__(self):
        return 'Weather setter class for %s weather provider' % self.wp.weather_provider

        
# Четыре последующих класса реализую свой собственный метод parse_to_dict, т.к. у прогнозных сайтов
# сильно разнятся API, а в базу данных weather_weather необходимо вносить данные в определенном виде
class WGRP5(WG):
    
    def parse_to_dict(self):
        weather_data = []
        
        if self.parsed_xml == -1:
            return weather_data
            
        def get_clouds_img(clouds, d):
            clouds_ranges = [
                xrange(0, 11),
                xrange(11, 31),
                xrange(31, 51),
                xrange(51, 71),
                xrange(71, 91),
                xrange(91, 101),
            ]
            for r in xrange(0, 6):
                if clouds in clouds_ranges[r]:
                    return self.file_name_prefix(d) + str(r) 
            
        def get_wd(wd):
            wds = {
                u'ШТЛ': -1,
                u'С': 0,
                u'С-В': 45,
                u'С-З': 315,
                u'Ю': 180,
                u'Ю-В': 135,
                u'Ю-З': 225,
                u'В': 90,
                u'З': 270
            }
            return wds[wd]
            
        def get_falls_img(falls, drops):
            global post_img
            pref_img = 't%sd' % falls
            if drops in ('0', '0.5', '1'):
                post_img = '0'
            elif drops in ('2', '3'):
                post_img = '1'
            elif drops in ('4', '5'):
                post_img = '2'
            elif drops in ('6', '7'):
                post_img = '3'
            elif drops in ('8', '9'):
                post_img = '4'
            return pref_img + post_img
        
        for day in self.node_value_get('timestep'):
            clouds = int(self.node_value_get('cloud_cover', node=day, subnode_num=0))
            tmp_data = {'wp': self.wp}
            d = self.node_value_get('datetime', node=day, subnode_num=0)
            tmp_data['datetime'] = datetime.strptime(d, self.format)
            tmp_data['clouds'] = clouds 
            tmp_data['precipitation'] = self.node_value_get('precipitation', node=day, subnode_num=0)
            tmp_data['temperature'] = self.node_value_get('temperature', node=day, subnode_num=0)
            tmp_data['pressure'] = self.node_value_get('pressure', node=day, subnode_num=0)
            tmp_data['humidity'] = self.node_value_get('humidity', node=day, subnode_num=0)
            tmp_data['wind_speed'] = self.node_value_get('wind_velocity', node=day, subnode_num=0)
            tmp_data['wind_direction'] = get_wd(self.node_value_get('wind_direction', node=day, subnode_num=0))
            tmp_data['clouds_img'] = get_clouds_img(clouds, tmp_data['datetime'])
            tmp_data['falls_img'] = get_falls_img(
                self.node_value_get('falls', node=day, subnode_num=0),
                self.node_value_get('drops', node=day, subnode_num=0)
            )
            weather_data.append(tmp_data)
            
        return weather_data

        
class WGWUA(WG):
    
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
                    return self.file_name_prefix(d) + str(num)
            
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

        for day in self.node_value_get('day')[:8]:
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

        
class WGYA(WG):
    
    def parse_to_dict(self):
        weather_data = []
        
        if self.parsed_xml == -1:
            return weather_data

        def get_wd(wd):
            wds = {
                'calm': -1,
                'n': 0,
                'ne': 45,
                'nw': 315,
                's': 180,
                'se': 135,
                'sw': 225,
                'e': 90,
                'w': 270,
            }
            return wds[wd]

        def get_file_img(weather_condition, d):
            weather_conditions = {
                'clear': ['0', 't0d0'],
                'mostly-clear': ['1', 't0d0'],
                'mostly-clear-slight-possibility-of-rain': ['1', 't1d0'],
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
                event_setter('system', u'Weather ya.ru: Неизвестные погодные условия %s' % weather_condition,
                             3, delay=3, sms=False)
                return [('na', 'na')]
            return [(
                    self.file_name_prefix(d) + weather_conditions[weather_condition][0],
                    weather_conditions[weather_condition][1]
                    )]
        
        times = {'morning': '07:00', 'day': '13:00', 'evening': '19:00', 'night': '01:00'}
        for day in self.node_value_get('day')[:2]:
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

        
class WGOWM(WG):
    
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
            if clouds not in clouds_ranges:
                return self.file_name_prefix(d) + '5'
            return self.file_name_prefix(d) + clouds_ranges[clouds]            
            
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
        for day in self.node_value_get('time')[:2]:
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
                tmp_data['wind_direction'] = self.node_value_get('windDirection', node=day, subnode_num=0, attr='deg')
                symbol_num = self.node_value_get('symbol', node=day, subnode_num=0, attr='number')
                tmp_data['clouds_img'] = get_clouds_img(symbol_num, tmp_data['datetime'])
                tmp_data['falls_img'] = get_falls_img(symbol_num)
                weather_data.append(tmp_data)
        
        return weather_data
 

def weather_getter(wp):
    """
    Выбор класса, соответствующего прогнозному сайту и запуск его метода

    :param wp: объект WeatherProvider, для которого будем парсить данные
    :returns: список из словарей погодных характеристик для различных временных точек
    """
    if wp.weather_provider == 'rp5':
        wg = WGRP5(wp)
    elif wp.weather_provider == 'wua':
        wg = WGWUA(wp)
    elif wp.weather_provider == 'ya':
        wg = WGYA(wp)
    elif wp.weather_provider == 'owm':
        wg = WGOWM(wp)
    else:
        return

    return wg.parse_to_dict()