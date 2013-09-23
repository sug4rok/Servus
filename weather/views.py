from base.views import call_template, get_weekday, get_month
from weather.models import Weather
from Servus.Servus import WEATHER_PROVIDERS
from datetime import datetime, timedelta

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
            clouds_data.append((clouds_img + '.png', clouds[num], clouds_range[clouds_img[2]], clouds_img[1]))
        return clouds_data
        
    def get_precipitation(wp):        
        precipitation_data = []
        precipitation = list_field_values(wp, 'precipitation')
        clouds_img = list_field_values(wp,'clouds_img')
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
            precipitation_data.append((falls_img + '.png', precipitation[num], falls_range[falls_img], clouds_img[num][1]))
        return precipitation_data
        
    def get_wind(wp):
        wind_data = []
        wind_speed = list_field_values(wp, 'wind_speed')
        for num, wind_direction in enumerate(list_field_values(wp, 'wind_direction')):
            wind_data.append((wind_speed[num], wind_direction))
        return wind_data
        
    def position_nearest_forecast():           
        datetimes = Weather.objects.all().values_list('datetime', flat=True)
        value_set = {
            'temperature':Weather.objects.all().values_list('temperature', flat=True),
            'wind_speed':Weather.objects.all().values_list('wind_speed', flat=True),
            'wind_direction':Weather.objects.all().values_list('wind_direction', flat=True),
            'clouds_img':Weather.objects.all().values_list('clouds_img', flat=True),
            'falls_img':Weather.objects.all().values_list('falls_img', flat=True)
        }
        
        tomorrow = (datetime.now() + timedelta(days=1)).day        
        indexes = []
        forecast_sidebar = {            
            'temperature':[],
            'wind_speed':[],
            'wind_direction':[],
            'clouds_img':[],
            'falls_img':[]
        }

        if len(datetimes):
            for num, d in enumerate(datetimes):
                if d.day == tomorrow and d.hour >= 13 and d.hour <=16:
                    for f in forecast_sidebar:                    
                        forecast_sidebar[f].append(value_set[f][num])
        else:
            return 'na'
            
        amount_data = len(forecast_sidebar['temperature'])
        for f in forecast_sidebar: 
            if f == 'falls_img':
                tmp_data1, tmp_data2 = 0, 0                    
                for i in range(amount_data):
                    tmp_data1 += int(forecast_sidebar[f][i][1])
                    tmp_data2 += int(forecast_sidebar[f][i][3])
                forecast_sidebar[f] = 't%sd%s' % (str(tmp_data1/amount_data), str(tmp_data2/amount_data))
            elif f == 'clouds_img':
                tmp_data1 = 0
                for i in range(amount_data):
                    tmp_data1 += int(forecast_sidebar[f][i][2])
                forecast_sidebar[f] = 'cd%s' % str(tmp_data1/amount_data)
            else:
                forecast_sidebar[f] = str(sum(forecast_sidebar[f])/amount_data)
        return forecast_sidebar
   
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
        
        pn.append('forecast')
        pv.append(forecast)
        pn.append('forecast_sidebar')
        pv.append(position_nearest_forecast())   
    
    return call_template(
        request,
        param_names = pn,
        param_vals = pv,
        current_tab=current_tab
    )