# coding=utf-8
from datetime import datetime, timedelta
from base.views import call_template
from climate.models import TempHumidSensor, TempHumidValue


def climate(request, current_tab):
    """
    Функция отображения грификов данных с климатических датчиков

    :param request: django request
    :param current_tab: название текущей вкладки (передается в Servus.urls)
    """

    sensors = TempHumidSensor.objects.filter(is_used=True)
    th_objs = list(TempHumidValue.objects.filter(sensor_datetime__gte=datetime.today() - timedelta(days=3)))

    temps, humids = [], []

    for s in sensors:
        sn = s.sensor_verb_name
        t, h = [], []
        for th in th_objs:
            if th.sensor_name_id == s.id:
                t.append((th.sensor_datetime.strftime('%Y, %m, %d, %H, %M'), th.temperature))
                h.append((th.sensor_datetime.strftime('%Y, %m, %d, %H, %M'), th.humidity))
        temps.append((sn, t))
        humids.append((sn, h))

    params = {'charts': (('температуры', '°C', temps), ('влажности', '%', humids))}

    return call_template(
        request,
        params,
        current_tab=current_tab
    )