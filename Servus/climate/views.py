# coding=utf-8
from datetime import datetime, timedelta
from base.views import call_template
from django.contrib.contenttypes.models import ContentType
from climate.models import TempHumidValue
from plugins.models import PLUGIN_MODELS


def climate(request, current_tab):
    """
    Функция отображения грификов данных с климатических датчиков

    :param request: django request
    :param current_tab: название текущей вкладки (передается в base.urls)
    """

    # Получаем все модели плагинов типа 'TempHumidSensor'
    th_sensors = filter(lambda s: s.TYPE == 'TempHumidSensor', PLUGIN_MODELS['climate'])
    
    # Для каждой модели типа 'TempHumidSensor' получаем список подключенных объектов (is_used=True)
    # и добавляем их в один кортеж.
    th_sensors_used = reduce(lambda res, s: res + tuple(s.objects.filter(is_used=True)), th_sensors, ())
    
    values = TempHumidValue.objects.filter(datetime__gte=datetime.today() - timedelta(days=3)).order_by('datetime')

    temps, humids = [], []

    for s in th_sensors_used:
        s_v = values.filter(content_type_id=ContentType.objects.get_for_model(s).id, object_id=s.id)
        temps.append((s.location, ((i.datetime, i.temperature) for i in s_v)))
        humids.append((s.location, ((i.datetime, i.humidity) for i in s_v)))

    params = {'charts': (('температуры', '°C', temps), ('влажности', '%', humids))}

    return call_template(
        request,
        params,
        current_tab=current_tab
    )
