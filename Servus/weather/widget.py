# coding=utf-8
from datetime import datetime, timedelta
from django.contrib.contenttypes.models import ContentType
from plugins.utils import get_plugins
from .models import WeatherValue
from .utils import CLOUDS_RANGE, FALLS_RANGE


def common_forecast(date):
    """
    Функция получения некоторых усредненных данных прогноза погоды для активированных погодных API,
    отображаемых на Главной странице.
    :param date: datetime День, для которого будем усреднять прогноз.
    :returns: словарь, с данными о температуре, скорости ветра и соответствующим облачности и
    осадкам файлам PNG.
    """

    # Создаем список объектов Weather, всех активированных прогнозных API,
    # приходящихся на переданный в функциию день с 12:00 до 16:00 включительно
    # (будем считать, что день у нас с 12 до 16 часов ;)).
    dt1 = datetime(date.year, date.month, date.day, 12)
    dt2 = datetime(date.year, date.month, date.day, 16)
    
    # Получаем все модели плагинов типа 'Forecast'
    f_objs = get_plugins('Forecast')

    # Для каждой модели типа 'Forecast' получаем список подключенных объектов (is_used=True),
    # учавствующих в усреднении (on_sidebar=True) и добавляем их в один кортеж.
    f_objs_used = reduce(lambda res, f: res + tuple(f.objects.filter(
        is_used=True, on_sidebar=True)), f_objs, ())

    # Для каждого объекта forecast получаем последние данные из таблицы weather_weathervalue.
    w_objs = reduce(lambda res, f: res + tuple(WeatherValue.objects.filter(
        content_type_id=ContentType.objects.get_for_model(f).id, object_id=f.id, datetime__range=[dt1, dt2])),
        f_objs_used, ())

    amount_data = len(w_objs)
    if amount_data:
        forecast = {'temperature': [], 'wind_speed': [], 'clouds_img': [], 'falls_img': [], 'wind_direction': []}
        
        for f in forecast:
            for o in w_objs:
                forecast[f].append(getattr(o, f))
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
    forecast['day'] = date.strftime('%d %b')
    return forecast


def get_widget_data():
    """
    Функция для получения данных для отображение краткой сводки прогноза погоды на сегодня и завтра
    на Главной странице
    :return: list Погодные данные
    """

    return common_forecast(datetime.today()), common_forecast(datetime.today() + timedelta(days=1))
