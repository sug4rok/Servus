# coding=utf-8
from datetime import datetime, timedelta
from base.views import call_template
from climate.models import TempHumidSensor, TempHumidValue, TempHumidValueShort


def climate(request, current_tab):
    """
    Функция отображения грификов данных с климатических датчиков

    :param request: django request
    :param current_tab: название текущей вкладки (передается в base.urls)
    """

    sensors = TempHumidSensor.objects.filter(is_used=True)
    values = TempHumidValue.objects.filter(datetime__gte=datetime.today() - timedelta(days=3)).order_by('datetime')

    temps, humids = [], []

    for s in sensors:
        sn = s.location
        sv = values.filter(sensor=s)
        temps.append((sn, ((i.datetime, i.temperature) for i in sv)))
        humids.append((sn, ((i.datetime, i.humidity) for i in sv)))

    params = {'charts': (('температуры', '°C', temps), ('влажности', '%', humids))}

    return call_template(
        request,
        params,
        current_tab=current_tab
    )


def get_temp_humid():
    """
    Получение данных о текущей температуре и влажности из таблицы climate_temphumidvalue БД
    :returns: список кортежей вида [(<полное имя датчика>, влажность, тепмпература), ...]
    """

    th_objs = TempHumidValueShort.objects.filter(sensor__is_used=True)
    return [(th_obj.sensor.location, th_obj.humidity, th_obj.temperature) for th_obj in th_objs]


def widget():
    """
    Функция для получения данных для отображение текущего значения температуры и влажности в помещениях
    на Главной странице
    :return: list Данные с датчиков температуры и влажности
    """

    return get_temp_humid()
