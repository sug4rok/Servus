# coding=utf-8
from datetime import datetime, timedelta
from base.views import call_template
from climate.models import TempHumidSensor, TempHumidValue


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
