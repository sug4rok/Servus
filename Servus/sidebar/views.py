# coding=utf-8
from datetime import datetime, timedelta
from base.views import call_template, get_events_short
from weather.models import Weather
from weather.views import CLOUDS_RANGE, FALLS_RANGE


def position_nearest_forecast():
        """
        Функция получения некоторых усредненных данных прогноза погоды для активированных погодных API,
        отображаемых на сайдбаре.
        На выходе: словарь, вида с данными о температуре, скорости ветра и соответствующим облачности и
        осадкам файлам PNG.
        """

        datetimes = Weather.objects.filter(wp__on_sidebar=True).values_list('datetime', flat=True)
        value_set = {
            'temperature': Weather.objects.filter(wp__on_sidebar=True).values_list('temperature', flat=True),
            'wind_speed': Weather.objects.filter(wp__on_sidebar=True).values_list('wind_speed', flat=True),
            'clouds_img': Weather.objects.filter(wp__on_sidebar=True).values_list('clouds_img', flat=True),
            'falls_img': Weather.objects.filter(wp__on_sidebar=True).values_list('falls_img', flat=True)
        }

        tomorrow = (datetime.now() + timedelta(days=1)).day 
        forecast_sidebar = {
            'temperature': [],
            'wind_speed': [],
            'clouds_img': [],
            'falls_img': []
        }

        # Создаем список порядковых номеров данных, всех активированных прогнозных API,
        # приходящихся относительно текущего времени на следующий день с 12:00 до 16:00 включительно
        #(будем считать, что день у нас с 12 до 16 часов ;)).
        if len(datetimes):
            for num, d in enumerate(datetimes):
                if d.day == tomorrow and 12 <= d.hour <= 16:
                    for f_k, f_v in forecast_sidebar.iteritems():
                        f_v.append(value_set[f_k][num])
        else:
            return 'na'

        # Определяем количество данных для усреднения
        amount_data = len(forecast_sidebar['temperature'])
        temperature = int(round(float(sum(forecast_sidebar['temperature'])) / amount_data, 0))

        # Заполняем словарь forecast_sidebar усредненными данными (данные выбираются согласно
        # составленному ранее списку валидных порядковых номеров данных после выборки из базы
        if amount_data:
            for f_k, f_v in forecast_sidebar.iteritems():
                if f_k == 'falls_img':
                    tmp_data1, tmp_data2 = 0.0, 0.0
                    for i in xrange(amount_data):
                        # Тип float необходим для правильного последующего округления после усреднения данных
                        tmp_data1 += float(f_v[i][1])
                        tmp_data2 += float(f_v[i][3])
                    if round(tmp_data1 / amount_data, 0):
                        if temperature > 2:
                            tmp_data1 = '1'
                        elif temperature < 0:
                            tmp_data1 = '3'
                        else:
                            tmp_data1 = '2'
                    else:
                        tmp_data1 = '0'
                    file_img = 't%sd%s' % (tmp_data1, str(int(round(tmp_data2 / amount_data, 0))))
                    forecast_sidebar[f_k] = [(file_img, FALLS_RANGE[file_img])]
                elif f_k == 'clouds_img':
                    tmp_data1 = 0.0
                    for i in xrange(amount_data):
                        tmp_data1 += float(f_v[i][2])
                    file_img = 'cd%s' % str(int(round(tmp_data1 / amount_data, 0)))
                    forecast_sidebar[f_k] = [(file_img, CLOUDS_RANGE[file_img[2]])]
                elif f_k == 'temperature':
                    forecast_sidebar[f_k] = str(temperature)
                else:
                    forecast_sidebar[f_k] = str(int(round(float(sum(f_v)) / amount_data, 0)))
        return forecast_sidebar


def sidebar(request):
    params = {
        'forecast_sidebar': position_nearest_forecast(),
        'amount_events': get_events_short(request)[0],
        'event_imp': get_events_short(request)[1]
    }

    return call_template(
        request,
        params,
        templ_path='base/sidebar.html'
    )