# coding=utf-8
from datetime import datetime, timedelta

from django.contrib.contenttypes.models import ContentType

from base.views import call_template
from plugins.utils import get_used_plugins_by
from climate.models import TempHumidValue


def climate(request):
    """
    Функция отображения грификов данных с климатических датчиков

    :param request: django request
    """

    th_sensors = get_used_plugins_by(plugin_type='TempHumidSensor')
    
    values = TempHumidValue.objects.filter(datetime__gte=datetime.today() - timedelta(days=3)).order_by('datetime')

    temps, humids = [], []

    for s in th_sensors:
        s_v = values.filter(content_type_id=ContentType.objects.get_for_model(s).id, object_id=s.id)
        temps.append((s.location, ((i.datetime, i.temperature) for i in s_v)))
        humids.append((s.location, ((i.datetime, i.humidity) for i in s_v)))

    params = {'active_app_name': 'climate', 'charts': (('температуры', '°C', temps), ('влажности', '%', humids))}

    return call_template(request, params)
