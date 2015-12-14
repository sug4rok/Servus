# coding=utf-8
from datetime import datetime, timedelta

from django.contrib.contenttypes.models import ContentType

from base.views import call_template
from plugins.utils import get_used_plugins_by
from climate.models import TempHumidValue, PressureValue


def get_climate_data(sensors, value_model, attr):
    """
    Функция представляет определенные (параметр attr) климатические данные за последние
    трое суток в нужном формате.

    :param sensors: list Список объектов климатических сенсоров.
    :param value_model: object Модель для хранения климатических данных.
    :param attr: str Атрибут объекта данных ('temperature', 'humidity', etc.)
    :returns: list Список данных для отображения в виде графика на вкладке
    Климат. Формат: [('расположение', ((дата1, значение1), (дата2, значение2), ...)]
    """

    values = value_model.objects.filter(datetime__gte=datetime.today() - timedelta(days=3)).order_by('datetime')

    lst = []

    for sensor in sensors:
        s_v = values.filter(content_type_id=ContentType.objects.get_for_model(sensor).id,
                            object_id=sensor.id)
        lst.append((sensor.location, ((i.datetime, getattr(i, attr)) for i in s_v)))

    return lst


def climate(request):
    """
    Функция вывода необходимых вкладке Климат данных с климатических датчиков, названий
    единиц измерения, название вкладки и пр.

    :param request: django request
    """

    th_sensors = get_used_plugins_by(plugin_type='TempHumidSensor')
    temps = get_climate_data(th_sensors, TempHumidValue, 'temperature')
    humids = get_climate_data(th_sensors, TempHumidValue, 'humidity')

    p_sensors = get_used_plugins_by(plugin_type='PressureSensor')
    pressures = get_climate_data(p_sensors, PressureValue, 'pressure')

    params = {'active_app_name': 'climate', 'charts': (('temp_div', 'температуры', '°C', temps),
                                                       ('hum_div', 'влажности', '%', humids),
                                                       ('press_div', 'атмосферного давления', 'мм рт.ст.', pressures))}

    return call_template(request, params)
