# coding=utf-8
from climate.models import TempHumidSensor, TempHumidValue


def get_widget_data():
    """
    Получение данных о текущей температуре и влажности из таблицы climate_temphumidvalue БД
    :returns: список кортежей вида [(<полное имя датчика>, влажность, тепмпература), ...]
    """

    sensors = TempHumidSensor.objects.filter(is_used=True)
    th_objs = [TempHumidValue.objects.filter(sensor=s).order_by('-datetime')[0] for s in sensors]
    return [(th_obj.sensor.location, th_obj.humidity, th_obj.temperature) for th_obj in th_objs]
