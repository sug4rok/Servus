from xml.dom import minidom
import urllib2


class WG(object):
    '''
    Класс, реализующий доставку прогноза погоды с XML-API прогнозных сайтов в таблицу weather_weather
    базы данных. Функция parse_to_dict реализуется в каждом классе-потомке отдельно, т.к. 
    у каждого прогнозного сайта свой API и парсинг XML-данных уникален.
    На входе: кодовое обозначение прогнозного сайта, например 'rp5'
    '''    
    def __init__(self, wp):
        self.wp = wp  
    
    def weather_get(self):       
        url_sock = urllib2.urlopen(self.wp_url)
        parsed_xml = minidom.parse(url_sock)                  
        url_sock.close()
        return self.parse_to_dict(parsed_xml)
    
    def __str__(self):
        return 'Weather setter class for %s weather provider' % self.wp

        
# Четыре последующих класса реализую свой собственный метод parse_to_dict, т.к. у прогнозных сайтов
# сильно разнятся API, а в базу данных weather_weather необходимо вносить данные в определенном виде
class WG_RP5(WG):
    wp_url = 'http://rp5.ru/xml/7285/00000/ru'   
    
    def parse_to_dict(self, parsed_xml):

        def point_name_get(tag_name, i):
            point_names = parsed_xml.getElementsByTagName(tag_name)
            return point_names[i-1].childNodes[0].nodeValue
            
        def get_clouds_img(clouds):
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
                    return r
            
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
        
        weather_data = []
        for i in range(1,5):
            clouds = int(point_name_get('cloud_cover', i))
            tmp_data = {}
            tmp_data['weather_provider'] = 'rp5'
            tmp_data['datetime'] = point_name_get('datetime', i)
            tmp_data['clouds'] = clouds 
            tmp_data['precipitation'] = point_name_get('precipitation', i)
            tmp_data['temperature'] = point_name_get('temperature', i)
            tmp_data['pressure'] = point_name_get('pressure', i)
            tmp_data['humidity'] = point_name_get('humidity', i)
            tmp_data['wind_speed'] = point_name_get('wind_velocity', i)
            tmp_data['wind_direction'] = get_wd(point_name_get('wind_direction', i))
            tmp_data['clouds_img'] = get_clouds_img(clouds)
            tmp_data['falls_img'] = get_falls_img(point_name_get('falls', i), point_name_get('drops', i))          
            weather_data.append(tmp_data)
            
        return weather_data

        
class WG_WUA(WG):
    wp_url = 'http://xml.weather.co.ua/1.2/forecast/773?dayf=4?lang=ru'
    
    def parse_to_dict(self, i):
        return weather_data

        
class WG_YA(WG):
    wp_url = 'http://export.yandex.ru/weather-ng/forecasts/26063.xml'
    weather_data = {} 
    
    def parse_to_dict(self, i):
        return weather_data

        
class WG_OWM(WG):
    wp_url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=St.Petersburg&mode=xml&units=metric&cnt=4'
    weather_data = {} 
    
    def parse_to_dict(self, i):
        return weather_data
 

         
def weather_getter(wp):
    '''
    Выбор класса, соответствующего прогнозному сайту и запуск его метода
    На входе: прогнозный сайт (берется из настроек Servus.Servus), например 'rp5'
    На выходе: ничего не возвращается, пишется в базу weather_weather
    '''      
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
        
    return wg.weather_get()