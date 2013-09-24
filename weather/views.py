from base.views import call_template, get_weekday, get_month
from weather.models import Weather
from Servus.Servus import WEATHER_PROVIDERS
from datetime import datetime, timedelta

params = {}

def weather(request, current_tab):
    pn, pv = [], []
    clouds_range = {
        '0':'Ясно',
        '1':'Малооблачно',
        '2':'Переменная облачность',
        '3':'Облачно с прояснениями',
        '4':'Облачно',
        '5':'Пасмурная погода',
        'na':'Нет данных'
    }
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
        'na':'Нет данных'
    }  
    
       
    def list_field_values(wp, field):
        ''' 
        Функция получения данных из базы для определенного прогнозного API и указанного поля
        На входе: 
            - название прогнозного api из Servus.Servus, например 'rp5'
            - поле таблицы базы данных, например 'clouds'
        На выходе: список даанных указанного поля
        '''   
        return Weather.objects.filter(weather_provider=wp).values_list(field, flat=True)

    def get_field_data(wp, field, measure):
        '''
        Базовая функция, возвращающая набор данных в определенном порядке для шаблона weather/tab.html
        На входе:
            - название прогнозного api из Servus.Servus, например 'rp5'
            - поле таблицы базы данных, например 'temperature'
            - еденица измерения
        На выходе: кортеж, вида (<имя поля>, <описание>, <ед. измерения>, [(список значений поля]))
        '''        
        return (
            field.name,
            field.verbose_name,
            measure,
            list_field_values(wp, field.name)
        )
    
    def get_forecast_time(wp):        
        '''
        Функция, возвращающая кортеж с данными о времени для определенного погодного API.
        На входе: название прогнозного api из Servus.Servus, например 'owm'
        На выходе: кортеж, вида (<день недели>, <день> <месяц>, <час:00>)
        '''
        forecast_times = []
        for forecast_time in list_field_values(wp, 'datetime'): 
            forecast_times.append((
                get_weekday(forecast_time.weekday()),
                '%s %s' % ((forecast_time.day), get_month(forecast_time.month)),
                '%s:00' % str(forecast_time.hour)
            ))
        return forecast_times
        
    def get_clouds(wp): 
        '''
        Функция, возвращающая кортеж с данными об обланчости, включая название соответствующего
        облачности файл PNG.
        На входе: название прогнозного api из Servus.Servus, например 'ya'
        На выходе: кортеж, вида (<файл png>, <облачность в %> <описание>, <время суток>)
        , где <время суток> - 'd' или 'n' (соответсвенно день, или ночь), используется для
        затемнения "ночных" ячеек таблицы.
        '''
        clouds_data = []
        clouds = list_field_values(wp, 'clouds')        
        for num, clouds_img in enumerate(list_field_values(wp,'clouds_img')):
            if clouds_img != 'na':
                clouds_data.append((clouds_img + '.png', clouds[num], clouds_range[clouds_img[2]], clouds_img[1]))
            else:
                clouds_data.append((clouds_img + '.png', clouds[num], clouds_range[clouds_img], 'd'))
        return clouds_data
        
    def get_precipitation(wp):   
        '''
        Функция, возвращающая кортеж с данными об осадках, включая название соответствующего
        количеству осадков файл PNG.
        На входе: название прогнозного api из Servus.Servus, например 'wua'
        На выходе: кортеж, вида (<файл png>, <количество выпавших осадков в мм>, <описание>, <время суток>)
        , где <время суток> - 'd' или 'n' (соответсвенно день, или ночь), используется для
        затемнения "ночных" ячеек таблицы.
        '''    
        precipitation_data = []
        precipitation = list_field_values(wp, 'precipitation')
        clouds_img = list_field_values(wp,'clouds_img')
        for num, falls_img in enumerate(list_field_values(wp, 'falls_img')):
            if falls_img != 'na':
                precipitation_data.append((falls_img + '.png', precipitation[num], falls_range[falls_img], clouds_img[num][1]))
            else:
                precipitation_data.append((falls_img + '.png', precipitation[num], falls_range[falls_img], 'd'))
        return precipitation_data
        
    def get_wind(wp):
        '''
        Функция, возвращающая кортеж с данными о ветре для определенного погодного API.
        На входе: название прогнозного api из Servus.Servus, например 'owm'
        На выходе: кортеж, вида (<скорость ветра>, <направление ветра в градусах>)
        '''
        wind_data = []
        wind_speed = list_field_values(wp, 'wind_speed')
        for num, wind_direction in enumerate(list_field_values(wp, 'wind_direction')):
            wind_data.append((wind_speed[num], wind_direction))
        return wind_data
        
    def position_nearest_forecast():  
        '''
        Функция получения некоторых усредненных данных прогноза погоды для активированных погодных API,
        отображаемых на сайдбаре.
        На выходе: словарь, вида с данными о температуре, скорости ветра и соответствующим облачности и
        осадкам файлам PNG.
        '''
        datetimes = Weather.objects.all().values_list('datetime', flat=True)
        value_set = {
            'temperature':Weather.objects.all().values_list('temperature', flat=True),
            'wind_speed':Weather.objects.all().values_list('wind_speed', flat=True),            
            'clouds_img':Weather.objects.all().values_list('clouds_img', flat=True),
            'falls_img':Weather.objects.all().values_list('falls_img', flat=True)
        }
        
        tomorrow = (datetime.now() + timedelta(days=1)).day        
        indexes = []
        forecast_sidebar = {            
            'temperature':[],
            'wind_speed':[],
            'clouds_img':[],
            'falls_img':[]
        }

        # Создаем список порядковых номеров данных, всех активированных прогнозных API,
        # приходящихся относительно текущего времени на следующий день с 12:00 до 16:00 включительно
        #(будем считать, что день у нас с 12 до 16 часов ;)).
        if len(datetimes):
            for num, d in enumerate(datetimes):
                if d.day == tomorrow and d.hour >= 12 and d.hour <=16:
                    for f in forecast_sidebar:                    
                        forecast_sidebar[f].append(value_set[f][num])
        else:
            return 'na'
        
        # Определяем количество данных для усреднения
        amount_data = len(forecast_sidebar['temperature'])
        
        # Заполняем словарь forecast_sidebar усредненными данными (данные выбираются согласно
        # составленному ранее списку валидных порядковых номеров данных после выборки из базы
        for f in forecast_sidebar: 
            if f == 'falls_img':
                tmp_data1, tmp_data2 = 0, 0                    
                for i in range(amount_data):
                    # Тип float необходим для правильного последующего округления после усреднения данных
                    tmp_data1 += float(forecast_sidebar[f][i][1])
                    tmp_data2 += float(forecast_sidebar[f][i][3])
                file_img = 't%sd%s' % (str(int(round(tmp_data1/amount_data, 0))), str(int(round(tmp_data2/amount_data, 0))))
                forecast_sidebar[f] = [(file_img, falls_range[file_img])]
            elif f == 'clouds_img':
                tmp_data1 = 0
                for i in range(amount_data):
                    tmp_data1 += float(forecast_sidebar[f][i][2])                
                file_img = 'cd%s' % str(int(round(tmp_data1/amount_data, 0)))
                forecast_sidebar[f] = [(file_img, clouds_range[file_img[2]])]
            else:
                print f, forecast_sidebar[f], float(sum(forecast_sidebar[f])), amount_data, float(sum(forecast_sidebar[f]))/amount_data, round(float(sum(forecast_sidebar[f]))/amount_data, 0)
                forecast_sidebar[f] = str(int(round(float(sum(forecast_sidebar[f]))/amount_data, 0)))
        return forecast_sidebar
   
    forecast = []    
    fields = Weather._meta.fields
    
    if WEATHER_PROVIDERS:
        # Если хотябы один прогнозный API активирован, собираем список данных для передачи в шаблон.
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