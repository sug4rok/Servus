# coding=utf-8
from datetime import datetime, timedelta

from django.contrib.contenttypes.models import ContentType

from base.views import call_template
from plugins.utils import get_used_plugins_by
from climate.models import TempHumidValue, PressureValue, AmbientLightValue, RaindropValue


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

    result = []
    number_of_days = 3  # Количество дней, за которые выводятся данные
    number_of_results = 300  # Не более 300 результатов на графике для каждого сенсора

    # Создаем запрос на все данные не старше трех дней
    last_days = datetime.today() - timedelta(days=number_of_days)
    qs = value_model.objects.filter(datetime__gte=last_days).order_by('datetime')

    for sensor in sensors:
        # Отфильтровываем результаты по каждому сенсору
        qs_s = qs.filter(content_type_id=ContentType.objects.get_for_model(sensor).id,
                         object_id=sensor.id)

        # Расчитываем шаг для сокращения количества результатов и урезаем запрос
        step = int(round(len(qs_s) / float(number_of_results), 0))
        qs_s = qs_s[::step if step else 1]

        result.append((sensor.location, ((i.datetime, getattr(i, attr)) for i in qs_s)))

    return result


def climate(request):
    """
    Функция вывода необходимых вкладке Климат данных с климатических датчиков, названий
    единиц измерения, название вкладки и пр.

    :param request: django request
    """

    charts = []

    # Данные для графиков температуры и влажности
    th_sensors = get_used_plugins_by(plugin_type='TempHumidSensor')
    if th_sensors:
        temps = get_climate_data(th_sensors, TempHumidValue, 'temperature')
        humids = get_climate_data(th_sensors, TempHumidValue, 'humidity')
        if temps:
            charts.append(('temp_div', 'температуры', '°C', temps))
        if humids:
            charts.append(('hum_div', 'влажности', '%', humids))

    # Данные для графика атмосферного давления
    p_sensors = get_used_plugins_by(plugin_type='PressureSensor')
    if p_sensors:
        pressures = get_climate_data(p_sensors, PressureValue, 'pressure')
        if pressures:
            charts.append(('press_div', 'атмосферного давления', 'мм рт.ст.', pressures))

    # Данные для графиков освещенности
    al_sensors = get_used_plugins_by(plugin_type='AmbientLightSensor')
    if al_sensors:
        ambient_lights = get_climate_data(al_sensors, AmbientLightValue, 'ambient_light')
        if ambient_lights:
            charts.append(('ambl_div', 'освещенности', 'лк', ambient_lights))

    # Данные для графиков выпадения осадков
    rd_sensors = get_used_plugins_by(plugin_type='RaindropSensor')
    if rd_sensors:
        raindrops = get_climate_data(rd_sensors, RaindropValue, 'raindrop')
        if raindrops:
            charts.append(('rd_div', 'выпадения осадков', 'ед', raindrops))

    params = {'active_app_name': 'climate', 'charts': charts}

    return call_template(request, params)
