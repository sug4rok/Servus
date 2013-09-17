from base.views import call_template, get_weekday, get_month
from weather.models import Weather
from Servus.Servus import WEATHER_PROVIDERS

params = {}

def weather(request, current_tab):

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
        forecast_hours = list_field_values(wp, 'datetime')
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
            file_img = ''
            if forecast_hours[num].hour > 9 and forecast_hours[num].hour <= 20:
                file_img = 'cd%s.png' % clouds_img
            else:
                file_img = 'cn%s.png' % clouds_img
            clouds_data.append((file_img, clouds[num], clouds_range[clouds_img]))
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
   
    forecast = []
    fields = Weather._meta.fields
    
    if WEATHER_PROVIDERS:
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
                
    return call_template(
        request,
        param_name = 'forecast',
        param_val = forecast,
        current_tab=current_tab
    )