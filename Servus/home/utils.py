# coding=utf-8
from datetime import datetime, timedelta
from climate.models import TempHumidValueShort
from weather.models import Weather
from weather.views import CLOUDS_RANGE, FALLS_RANGE


def nearest_forecast(day):
        """
        Функция получения некоторых усредненных данных прогноза погоды для активированных погодных API,
        отображаемых на Главной странице.

        :param day: день ('сегодня' | 'завтра'), для которого будем усреднять прогноз.
        :returns: словарь, с данными о температуре, скорости ветра и соответствующим облачности и
        осадкам файлам PNG.
        """

        if day == 'сегодня':
            d = datetime.today()
        else:
            d = datetime.today() + timedelta(days=1)

        # Создаем список объектов Weather, всех активированных прогнозных API,
        # приходящихся на переданный в функциию день с 12:00 до 16:00 включительно
        #(будем считать, что день у нас с 12 до 16 часов ;)).
        dt1 = datetime(d.year, d.month, d.day, 12)
        dt2 = datetime(d.year, d.month, d.day, 16)
        w_objs = Weather.objects.filter(wp__on_sidebar=True, datetime__range=[dt1, dt2])

        amount_data = len(w_objs)
        if amount_data:
            forecast = {
                'temperature': w_objs.values_list('temperature', flat=True),
                'wind_speed': w_objs.values_list('wind_speed', flat=True),
                'clouds_img': w_objs.values_list('clouds_img', flat=True),
                'falls_img': w_objs.values_list('falls_img', flat=True)
            }
        else:
            return None

        # Заполняем словарь forecast снова, теперь уже усредненными данными
        temperature = round(float(sum(forecast['temperature'])) / amount_data, 0)
        for f_k, f_v in forecast.iteritems():
            if f_k == 'falls_img':
                tmp_data1 = sum([float(f[1]) for f in f_v]) / amount_data

                if tmp_data1 > 0.5:
                    if temperature > 2:
                        tmp_data1 = '1'
                    elif temperature < 0:
                        tmp_data1 = '3'
                    else:
                        tmp_data1 = '2'
                    tmp_data2 = sum([float(f[3]) for f in f_v]) / amount_data
                else:
                    tmp_data1, tmp_data2 = '0', 0.0

                file_img = 't%sd%.0f' % (tmp_data1, tmp_data2)
                forecast[f_k] = [(file_img, FALLS_RANGE[file_img])]
            elif f_k == 'clouds_img':
                tmp_data1 = sum([float(f[2]) for f in f_v]) / amount_data
                file_img = 'cd%.0f' % tmp_data1
                forecast[f_k] = [(file_img, CLOUDS_RANGE[file_img[2]])]
            elif f_k == 'temperature':
                forecast[f_k] = '%d' % temperature
            else:
                forecast[f_k] = '%d' % round(float(sum(f_v)) / amount_data, 0)
        forecast['day'] = day
        return forecast


def get_temp_humid():
    """
    Получение данных о текущей температуре и влажности из таблицы climate_temphumidvalue БД

    :returns: список кортежей вида [(<полное имя датчика>, влажность, тепмпература), ...]
    """

    th_objs = TempHumidValueShort.objects.filter(sensor_name__is_used=True)

    return [(th_obj.sensor_name.sensor_verb_name, th_obj.humidity, th_obj.temperature) for th_obj in th_objs]