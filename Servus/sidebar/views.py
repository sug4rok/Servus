# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from base.views import call_template
from weather.models import Weather
from weather.views import CLOUDS_RANGE, FALLS_RANGE

def position_nearest_forecast():  
        """
        Функция получения некоторых усредненных данных прогноза погоды для активированных погодных API,
        отображаемых на сайдбаре.
        На выходе: словарь, вида с данными о температуре, скорости ветра и соответствующим облачности и
        осадкам файлам PNG.
        """
        datetimes = Weather.objects.all().values_list('datetime', flat=True)
        value_set = {
            'temperature':Weather.objects.all().values_list('temperature', flat=True),
            'wind_speed':Weather.objects.all().values_list('wind_speed', flat=True),            
            'clouds_img':Weather.objects.all().values_list('clouds_img', flat=True),
            'falls_img':Weather.objects.all().values_list('falls_img', flat=True)
        }
        
        tomorrow = (datetime.now() + timedelta(days=1)).day 
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
        if amount_data:            
            for f in forecast_sidebar: 
                if f == 'falls_img':
                    tmp_data1, tmp_data2 = 0, 0                    
                    for i in range(amount_data):
                        # Тип float необходим для правильного последующего округления после усреднения данных
                        tmp_data1 += float(forecast_sidebar[f][i][1])
                        tmp_data2 += float(forecast_sidebar[f][i][3])
                    file_img = 't%sd%s' % (str(int(round(tmp_data1/amount_data, 0))), str(int(round(tmp_data2/amount_data, 0))))
                    forecast_sidebar[f] = [(file_img, FALLS_RANGE[file_img])]
                elif f == 'clouds_img':
                    tmp_data1 = 0
                    for i in range(amount_data):
                        tmp_data1 += float(forecast_sidebar[f][i][2])                
                    file_img = 'cd%s' % str(int(round(tmp_data1/amount_data, 0)))
                    forecast_sidebar[f] = [(file_img, CLOUDS_RANGE[file_img[2]])]
                else:
                    forecast_sidebar[f] = str(int(round(float(sum(forecast_sidebar[f]))/amount_data, 0)))            
        return forecast_sidebar
        
        
def sidebar(request):
    pn, pv = [], []
        
    pn.append('forecast_sidebar')
    pv.append(position_nearest_forecast())
    
    return call_template(
        request,
        param_names = pn,
        param_vals = pv,
        templ_path = 'base/sidebar.html'
    )