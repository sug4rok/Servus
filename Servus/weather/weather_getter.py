from xml.dom import minidom
import urllib2
from datetime import datetime, timedelta


class WG(object):
    """
    Класс, реализующий доставку прогноза погоды с XML-API прогнозных сайтов в таблицу weather_weather
    базы данных. Функция parse_to_dict реализуется в каждом классе-потомке отдельно, т.к. 
    у каждого прогнозного сайта свой API и парсинг XML-данных уникален.
    На входе: кодовое обозначение прогнозного сайта, например 'rp5'
    """    
    def __init__(self, wp):
        self.wp = wp
        self.parsed_xml = self.parse_xml()
        self.format = '%Y-%m-%d %H:%M'
        self.wp_url = None

    def parse_xml(self):
        url_sock = urllib2.urlopen(self.wp_url)
        parsed_xml = minidom.parse(url_sock)                  
        url_sock.close()
        return parsed_xml
    
    def tag_value_get(self, tag_name, i, *args):
        point_names = self.parsed_xml.getElementsByTagName(tag_name)
        if args:
            point_name = point_names[i-1].getElementsByTagName(args[0])
            return point_name[0].childNodes[0].nodeValue
        return point_names[i-1].childNodes[0].nodeValue

    def attr_value_get(self, tag_name, attr_name, i):
        point_names = self.parsed_xml.getElementsByTagName(tag_name)
        try:
            return point_names[i-1].attributes[attr_name].value
        except KeyError:
            return -1
        
    def file_name_prefix(self, d):
        hours_format = '%H'
        h = int(d.strftime(hours_format))
        if h > 8 and h <= 20:
            prefix = 'cd'
        else:
            prefix = 'cn'         
        return prefix 
    
    def __str__(self):
        return 'Weather setter class for %s weather provider' % self.wp

        
# Четыре последующих класса реализую свой собственный метод parse_to_dict, т.к. у прогнозных сайтов
# сильно разнятся API, а в базу данных weather_weather необходимо вносить данные в определенном виде
class WG_RP5(WG):
    wp_url = 'http://rp5.ru/xml/7285/00000/ru'   
    
    def parse_to_dict(self):
        weather_data = []
            
        def get_clouds_img(clouds, d):
            clouds_ranges = [
                range(0, 11),
                range(11, 31),
                range(31, 51),
                range(51, 71),
                range(71, 91),
                range(91, 101),
            ]
            for r in range(0, 6):
                if clouds in clouds_ranges[r]:
                    return self.file_name_prefix(d) + str(r) 
            
        def get_wd(wd):
            wds = {
                u'ШТЛ':-1,
                u'С':0,
                u'С-В':45,
                u'С-З':315,
                u'Ю':180,
                u'Ю-В':135,
                u'Ю-З':225,
                u'В':90,
                u'З':270
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
        
        for i in range(1,5):
            clouds = int(self.tag_value_get('cloud_cover', i))
            tmp_data = {'weather_provider': 'rp5'}
            d = self.tag_value_get('datetime', i)
            tmp_data['datetime'] = datetime.strptime(d, self.format)
            tmp_data['clouds'] = clouds 
            tmp_data['precipitation'] = self.tag_value_get('precipitation', i)
            tmp_data['temperature'] = self.tag_value_get('temperature', i)
            tmp_data['pressure'] = self.tag_value_get('pressure', i)
            tmp_data['humidity'] = self.tag_value_get('humidity', i)
            tmp_data['wind_speed'] = self.tag_value_get('wind_velocity', i)
            tmp_data['wind_direction'] = get_wd(self.tag_value_get('wind_direction', i))
            tmp_data['clouds_img'] = get_clouds_img(clouds, tmp_data['datetime'])
            tmp_data['falls_img'] = get_falls_img(self.tag_value_get('falls', i), self.tag_value_get('drops', i))          
            weather_data.append(tmp_data)
            
        return weather_data

        
class WG_WUA(WG):
    wp_url = 'http://xml.weather.co.ua/1.2/forecast/773?dayf=4?lang=ru'
    
    def parse_to_dict(self):
        weather_data = []

        def get_clouds_img(clouds, d):
            clouds_ranges = [
                range(0, 5),
                range(5, 10),
                range(10, 20),
                range(20, 25),
                range(25, 30),
                range(30, 101),
            ]
            for r in range(0, 6):
                if clouds in clouds_ranges[r]:
                    return self.file_name_prefix(d) + str(r)            
            
        def get_falls_img(clouds):
            falls_ranges = {
                't0d0':range(0, 40),
                't1d0':range(40, 50),
                't1d1':range(50, 52),
                't1d2':range(52, 55),
                't1d3':range(55, 58),
                't1d4':range(58, 60),
                't1d5':range(60, 70),
                't1d6':range(70, 80),
                't2d0':range(80, 82),
                't2d1':range(82, 84),
                't2d2':range(84, 86),
                't2d3':range(86, 88),
                't2d4':range(88, 90),
                't3d0':range(90, 92),
                't3d1':range(92, 94),
                't3d2':range(94, 96),
                't3d3':range(96, 98),
                't3d4':range(98, 100),
            }
            for r in falls_ranges:
                if clouds in falls_ranges[r]:
                    return r

        for i in range(1,9):
            clouds = int(self.tag_value_get('cloud', i))
            tmp_data = {'weather_provider': 'wua'}
            d = '%s %s:00' % (self.attr_value_get('day', 'date', i), self.attr_value_get('day', 'hour', i))
            tmp_data['datetime'] = datetime.strptime(d, self.format)
            tmp_data['temperature'] = int(self.tag_value_get('t', i+1, 'min')) + 1
            tmp_data['pressure'] = int(self.tag_value_get('p', i+1, 'min')) + 1
            tmp_data['humidity'] = int(self.tag_value_get('hmid', i, 'min')) + 1
            tmp_data['wind_speed'] = int(self.tag_value_get('wind', i, 'min')) + 1
            tmp_data['wind_direction'] = self.tag_value_get('rumb', i)
            tmp_data['clouds_img'] = get_clouds_img(clouds, tmp_data['datetime'])
            tmp_data['falls_img'] = get_falls_img(clouds)         
            weather_data.append(tmp_data)
        
        return weather_data

        
class WG_YA(WG):
    wp_url = 'http://export.yandex.ru/weather-ng/forecasts/26063.xml'
    
    def parse_to_dict(self):
        weather_data = []

        def get_wd(wd):
            wds = {
                u'calm':-1,
                u'n':0,
                u'ne':45,
                u'nw':315,
                u's':180,
                u'se':135,
                u'sw':225,
                u'e':90,
                u'w':270,
            }
            return wds[wd]

        def get_file_img(weather_condition, d):
            weather_conditions = {
                'clear':['0', 't0d0'],
                'mostly-clear':['1', 't0d0'],
                'mostly-clear-slight-possibility-of-rain':['1', 't1d0'],
                'partly-cloudy':['2', 't0d0'],
                'partly-cloudy-possible-thunderstorms-with-rain':['2', 't1d0'],
                'partly-cloudy-and-showers':['2', 't1d0'],
                'partly-cloudy-and-light-rain':['2', 't1d1'],
                'partly-cloudy-and-rain':['2', 't1d2'],
                'partly-cloudy-and-wet-snow-showers':['2', 't2d0'],
                'partly-cloudy-and-light-wet-snow':['2', 't2d1'],
                'partly-cloudy-and-wet-snow':['2', 't2d2'],
                'partly-cloudy-and-snow-showers':['2', 't3d0'],
                'partly-cloudy-and-light-snow':['2', 't3d1'],
                'partly-cloudy-and-snow':['2', 't3d2'],
                'cloudy':['3', 't0d0'],
                'cloudy-and-showers':['3', 't1d0'],
                'cloudy-and-light-rain':['3', 't1d1'],
                'cloudy-and-rain':['3', 't1d2'],
                'cloudy-thunderstorms-with-rain':['3', 't1d5'],
                'cloudy-and-wet-snow-showers':['3', 't2d0'],
                'cloudy-and-light-wet-snow':['3', 't2d1'],
                'cloudy-and-wet-snow':['3', 't2d2'],
                'cloudy-and-snow-showers':['3', 't3d0'],
                'cloudy-and-light-snow':['3', 't3d1'],
                'cloudy-and-snow':['3', 't3d2'],
                'overcast':['5', 't0d0'],
                'overcast-and-showers':['5', 't1d0'],
                'overcast-and-light-rain':['5', 't1d1'],
                'overcast-and-rain':['5', 't1d2'],
                'overcast-thunderstorms-with-rain':['5', 't1d5'],
                'overcast-and-wet-snow-showers':['5', 't2d0'],
                'overcast-and-light-wet-snow':['5', 't2d1'],
                'overcast-and-wet-snow':['5', 't2d2'],
                'overcast-and-snow-showers':['5', 't3d0'],
                'overcast-and-light-snow':['5', 't3d1'],
                'overcast-and-snow':['5', 't3d2'],
            }
            if weather_condition not in weather_conditions:
                return [('na', 'na')]
            return [(
                    self.file_name_prefix(d) + weather_conditions[weather_condition][0],
                    weather_conditions[weather_condition][1]
                    )]
        
        times = {'morning':'07:00', 'day':'13:00', 'evening':'19:00', 'night':'01:00'}
        for i in range(1, 3):
            day = self.attr_value_get('day', 'date', i)
            for j in range(1, 5):
                weather_condition = self.attr_value_get('weather_condition', 'code', j)
                tmp_data = {'weather_provider': 'ya'}
                part_of_day = self.attr_value_get('day_part', 'type', j)
                d = '%s %s' % (day, times[part_of_day])
                d_datetime = datetime.strptime(d, self.format)
                if part_of_day == 'night':
                    d_datetime += timedelta(days=1)
                tmp_data['datetime'] = d_datetime
                tmp_data['temperature'] = self.tag_value_get('avg', j)
                tmp_data['pressure'] = self.tag_value_get('pressure', j)
                tmp_data['humidity'] = self.tag_value_get('humidity', j)
                tmp_data['wind_speed'] = round(float(self.tag_value_get('wind_speed', j)), 0)
                tmp_data['wind_direction'] = get_wd(self.tag_value_get('wind_direction', j))
                for clouds_img, falls_img in get_file_img(weather_condition, tmp_data['datetime']):
                    tmp_data['clouds_img'] = clouds_img
                    tmp_data['falls_img'] = falls_img         
                    weather_data.append(tmp_data)
        return weather_data

        
class WG_OWM(WG):
    wp_url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=St.Petersburg&mode=xml&units=metric&cnt=4'
    
    def parse_to_dict(self):
        weather_data = []

        def get_clouds_img(clouds, d):
            clouds_ranges = {
                '800':'0',
                '801':'1',
                '802':'2',
                '803':'3',
                '804':'5',
            }
            if clouds not in clouds_ranges:
                return self.file_name_prefix(d) + '5'
            return self.file_name_prefix(d) + clouds_ranges[clouds]            
            
        def get_falls_img(clouds):
            falls_ranges = {
                't1d0':['321', '520', '521', '522'],
                't1d1':['200', '300', '310', '500'],
                't1d2':['201', '301', '311', '501'],
                't1d3':['202', '302', '312', '502'],
                't1d4':['210', '230', '503', '504'],
                't1d5':['211', '212', '221', '231', '232'],
                't1d6':['906'],
                't2d2':['511', '611'],
                't3d0':['621'],
                't3d2':['600'],
                't3d3':['601'],
                't3d4':['602']
            }
            for r in falls_ranges:
                if clouds in falls_ranges[r]:
                    return r
            return 't0d0'

        times = [('morn','07:00'), ('day','13:00'), ('eve','19:00'), ('night','01:00')] 
        for i in range(1,3):      
            for part_of_day, time in times:
                tmp_data = {'weather_provider': 'owm'}
                d =  '%s %s' % (self.attr_value_get('time', 'day', i), time)
                d_datetime = datetime.strptime(d, self.format)
                if part_of_day == 'night':
                    d_datetime += timedelta(days=1)
                tmp_data['datetime'] = d_datetime
                tmp_data['clouds'] = self.attr_value_get('clouds', 'all', i)
                precipitation = self.attr_value_get('precipitation', 'value', i)
                if precipitation != -1:
                    tmp_data['precipitation'] = precipitation
                tmp_data['temperature'] = round(float(self.attr_value_get('temperature', part_of_day, i)), 0)
                tmp_data['pressure'] = round(float(self.attr_value_get('pressure', 'value', i))/1.333224, 0)
                tmp_data['humidity'] = self.attr_value_get('humidity', 'value', i)
                tmp_data['wind_speed'] = round(float(self.attr_value_get('windSpeed', 'mps', i)), 0)
                tmp_data['wind_direction'] = self.attr_value_get('windDirection', 'deg', i)
                symbol_num = self.attr_value_get('symbol', 'number', i)
                tmp_data['clouds_img'] = get_clouds_img(symbol_num, tmp_data['datetime'])
                tmp_data['falls_img'] = get_falls_img(symbol_num)
                weather_data.append(tmp_data)
        
        return weather_data
 

         
def weather_getter(wp):
    """
    Выбор класса, соответствующего прогнозному сайту и запуск его метода
    На входе: прогнозный сайт (берется из настроек Servus.Servus), например 'rp5'
    На выходе: ничего не возвращается, пишется в базу weather_weather
    """      
    if wp == 'rp5':
        wg = WG_RP5(wp)      
    elif wp == 'wua':
        wg = WG_WUA(wp)        
    elif wp == 'ya':
        wg = WG_YA(wp)
    elif wp == 'owm':
        wg = WG_OWM(wp)
    else: 
        return
        
    return wg.parse_to_dict()