from base.views import call_template, get_weekday, get_month
from weather.models import Weather
from Servus.Servus import WEATHER_PROVIDERS
from datetime import datetime

params = {}

def weather(request, current_tab):
    pn, pv = [], []

    def list_field_values(wp, field):
        return Weather.objects.filter(weather_provider=wp).values_list(field, flat=True)

    def get_field_data(wp, field, measure):
        '''
        A simple function to retrieve data from a table rp5r for onward dispatch to the template
        '''        
        return (
            field.name,
            field.verbose_name,
            measure,
            list_field_values(wp, field.name)
        )
    
    def get_forecast_time(wp):        
        forecast_times = []
        for forecast_time in list_field_values(wp, 'datetime'): 
            forecast_times.append((
                get_weekday(forecast_time.weekday()),
                '%s %s' % ((forecast_time.day), get_month(forecast_time.month)),
                '%s:00' % str(forecast_time.hour)
            ))
        return forecast_times
        
    def get_clouds(wp):      
        clouds_data = []
        clouds = list_field_values(wp, 'clouds')
        clouds_range = {
            '0':'Ясно',
            '1':'Малооблачно',
            '2':'Переменная облачность',
            '3':'Облачно с прояснениями',
            '4':'Облачно',
            '5':'Пасмурная погода'
        }
        for num, clouds_img in enumerate(list_field_values(wp,'clouds_img')):
            clouds_data.append((clouds_img + '.png', clouds[num], clouds_range[clouds_img[2]]))
        return clouds_data
        
    def get_precipitation(wp):        
        precipitation_data = []
        precipitation = list_field_values(wp, 'precipitation')
        falls_range = {
            't0d0':'Без осадков',
            't1d0':'Кратковременный дождь',
            't1d1':'Небольшой дождь',
            't1d2':'Дождь',
            't1d3':'Сильный дождь',
            't1d4':'Ливень',
            't1d5':'Гроза',
            't2d0':'Кратковременный мокрый снег',
            't2d1':'Небольшой мокрый снег',
            't2d2':'Мокрый снег',
            't2d3':'Сильный мокрый снег',
            't2d4':'Метель',
            't3d0':'Кратковременный снег',
            't3d1':'Небольшой снег',
            't3d2':'Снег',
            't3d3':'Сильный снег',
            't3d4':'Метель',
        }        
        for num, falls_img in enumerate(list_field_values(wp, 'falls_img')):
            precipitation_data.append((falls_img + '.png', precipitation[num], falls_range[falls_img]))
        return precipitation_data
        
    def get_wind(wp):
        wind_data = []
        wind_speed = list_field_values(wp, 'wind_speed')
        for num, wind_direction in enumerate(list_field_values(wp, 'wind_direction')):
            wind_data.append((wind_speed[num], wind_direction))
        return wind_data
        
    def position_nearest_forecast(wp):
        now = datetime.now()
        forecast_times = list_field_values(wp, 'datetime')
        if len(forecast_times):
            for num, forecast_time in enumerate(forecast_times):
                if forecast_time > now:
                    return num
        else:
            return -1
   
    forecast = []
    forecast_sidebar = {
        'clouds_img':[],
        'falls_img':[],
        'temperature':[],
        'wind_speed':[],
        'wind_direction':[]
    }
    
    fields = Weather._meta.fields
    
    if WEATHER_PROVIDERS:
        # Вывод данных на страницу прогноза погоды
        for wp in WEATHER_PROVIDERS:
            value_set = []
            for field in fields[2:-3]:
                if field.name == 'datetime':
                    value_set.append((field.name, field.verbose_name, '', get_forecast_time(wp))) 
                elif field.name == 'clouds':
                    value_set.append((field.name, field.verbose_name, '', get_clouds(wp))) 
                elif field.name == 'precipitation':
                    value_set.append((field.name, field.verbose_name, '', get_precipitation(wp)))
                elif field.name == 'temperature':
                    value_set.append(get_field_data(wp, field, '°C'))
                elif field.name == 'pressure':
                    value_set.append(get_field_data(wp, field, 'мм рт. ст.'))
                elif field.name == 'humidity':
                    value_set.append(get_field_data(wp, field, '%'))
                elif field.name == 'wind_speed':
                    value_set.append((field.name, field.verbose_name, 'м/c', get_wind(wp)))
            forecast.append((WEATHER_PROVIDERS[wp], value_set))        
        
            num = position_nearest_forecast(wp)
            if num != -1:
                for f in forecast_sidebar:
                    forecast_sidebar[f].append(list_field_values(wp, f)[num])
        
        # Вывод усредненных данных прогноза погоды на sidebar
        len_forecast_field = len(forecast_sidebar['clouds_img'])
        if len_forecast_field:
            for f in forecast_sidebar:                
                if f == 'falls_img':
                    tmp_data1, tmp_data2 = 0, 0                    
                    for i in range(len_forecast_field):
                        tmp_data1 += int(forecast_sidebar[f][i][1])
                        tmp_data2 += int(forecast_sidebar[f][i][3])
                    forecast_sidebar[f] = 't%sd%s' % (str(tmp_data1/len_forecast_field), str(tmp_data2/len_forecast_field))
                elif f == 'clouds_img':
                    tmp_data1 = 0
                    tmp_data2 = forecast_sidebar[f][i][1]
                    for i in range(len_forecast_field):
                        tmp_data1 += int(forecast_sidebar[f][i][2])
                    forecast_sidebar[f] = 'c%s%s' % (tmp_data2, str(tmp_data1/len_forecast_field))
                else:
                    tmp_data = 0
                    for i in range(len_forecast_field):
                        tmp_data += int(forecast_sidebar[f][i])
                    forecast_sidebar[f] = str(tmp_data/len_forecast_field)
        
        pn.append('forecast')
        pv.append(forecast)
        pn.append('forecast_sidebar')
        pv.append(forecast_sidebar)   
    
    return call_template(
        request,
        param_names = pn,
        param_vals = pv,
        current_tab=current_tab
    )