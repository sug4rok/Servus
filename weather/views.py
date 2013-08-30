from base.views import *
from weather.models import RP5RU
from datetime import datetime, timedelta

def weather(request): 
    
    def get_field_data(field, measure):
        '''
        A simple function to retrieve data from a table rp5r for onward dispatch to the template
        '''
        
        return (
                field.name,
                field.verbose_name, 
                measure, 
                [values for values in RP5RU.objects.values_list(field.name, flat=True)]
                )
   
    def get_forecast_time():        
        forecast_times = []
        for forecast_time in RP5RU.objects.values_list('datetime', flat=True):            
            forecast_times.append((
                                   get_weekday(forecast_time.weekday()),
                                   '%s %s' % ((forecast_time.day), get_month(forecast_time.month)),
                                   '%s:00' % str(forecast_time.hour)
                                   ))
        return forecast_times

    def get_cloud_cover():
        '''
        Adding a prefixes to the filename ('cd' for day, 'cn' for night).
        Сonversion percentage of cloud cover in the range from 1 to 7.
        For example 35% cloud cover for time_step = 12 turn into a prefix 'cd3'
        '''
        
        cloud_cover = []
        forecast_hours = RP5RU.objects.values_list('datetime', flat=True)
        cloud_ranges = {
                        0:(range(0, 11), 'Ясно'),
                        1:(range(11, 21), 'Малооблачно'),
                        2:(range(21, 31), 'Небольшая облачность'),
                        3:(range(31, 51), 'Переменная облачность'),
                        4:(range(51, 71), 'Облачно с прояснениями'),
                        5:(range(71, 81), 'Облачно'),
                        6:(range(81, 91), 'Значительная облачность'),
                        7:(range(91, 100), 'Пасмурная погода')
                        }
        for num, cloud_percent in enumerate(RP5RU.objects.values_list('cloud_cover', flat=True)):
            file_prefix = ''
            if forecast_hours[num].hour == 4:
                file_prefix = 'cn'
            else:
                file_prefix = 'cd'
            for cloud_range in cloud_ranges:
                rng, descr = cloud_ranges[cloud_range]
                if cloud_percent in rng:
                    cloud_cover.append((file_prefix + str(cloud_range), cloud_percent, descr))
        return cloud_cover 

    def get_wind():
        '''
        Adding a prefixes to the filename ('wd_n', 'wd_se', etc) to get the corresponding
        GIF file for respective wind direction.        
        '''
        
        wind_data = []
        wind_velocity = RP5RU.objects.values_list('wind_velocity', flat=True)
        wind_directions = {
                           u'ШТЛ':('w0', 'Штиль'),
                           u'С':('wd_n', 'севера'),
                           u'С-В':('wd_ne', 'северо-востока'),
                           u'С-З':('wd_nw', 'северо-запада'),
                           u'Ю':('wd_s', 'юга'),
                           u'Ю-В':('wd_se', 'юго-востока'),
                           u'Ю-З':('wd_sw', 'юго-запада'),
                           u'В':('wd_e', 'востока'),
                           u'З':('wd_w', 'запада')
                          }         
        for num, wind_direction in enumerate(RP5RU.objects.values_list('wind_direction', flat=True)):
            wind_direction, descr = wind_directions[wind_direction]
            wind_data.append((wind_velocity[num], wind_direction, descr))
        return wind_data
        
    def get_precipitation():
        '''
        Adding 'oXdY a prefix to the file name to get the corresponding PNG file for precipitation,
        where X - type of precipitation, Y - the amount of precipitation.
        '''
        
        precipitation_data = []
        falls = RP5RU.objects.values_list('falls', flat=True)
        drops = RP5RU.objects.values_list('drops', flat=True)
        falls_range = {
                       0:'Без осадков',
                       1:'Дождь',
                       2:'Мокрый снег',
                       3:'Снег'
                      }        
        for num, precipitation in enumerate(RP5RU.objects.values_list('precipitation', flat=True)):
            precipitation_data.append(('o%sd%s' % (falls[num], drops[num]), precipitation, falls_range[falls[num]]))
        return precipitation_data
        
        
    rp5ru = []
    fields = RP5RU._meta.fields
    
    for field in fields[1:-1]:
        if field.name == 'datetime':
            rp5ru.append((field.name, field.verbose_name, '', get_forecast_time()))           
        elif field.name == 'cloud_cover':
            rp5ru.append((field.name, field.verbose_name, '', get_cloud_cover()))
        elif field.name == 'falls':
            pass
        elif field.name == 'precipitation':
            rp5ru.append((field.name, field.verbose_name, '', get_precipitation()))
        elif field.name == 'drops':
            pass
        elif field.name == 'temperature':
            rp5ru.append(get_field_data(field, '°C'))
        elif field.name == 'pressure':
            rp5ru.append(get_field_data(field, 'мм рт. ст.'))
        elif field.name == 'humidity':
            rp5ru.append(get_field_data(field, '%'))
        elif field.name == 'wind_velocity':
            rp5ru.append((field.name, field.verbose_name, 'м/c', get_wind()))      
      
    active_app_name = os.path.dirname(os.path.relpath(__file__))
    get_tab_options(active_app_name)    
    params['rp5ru'] = rp5ru
    return render_to_response('weather/tab.html', params)