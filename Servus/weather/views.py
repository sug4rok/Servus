# coding=utf-8
from base.views import call_template
from plugins.utils import get_plugins
from django.contrib.contenttypes.models import ContentType
from .models import WeatherValue
from .utils import CLOUDS_RANGE, FALLS_RANGE


def list_field_values(wp, field):
    """
    Функция получения данных из базы для определенного прогнозного API и указанного поля

    :param wp: id объекта WeatherProvider, для которого получаем данные
    :param field: поле таблицы базы данных, например 'clouds'
    :returns: генератор списка данных указанного поля
    """

    return WeatherValue.objects.filter(content_type_id=ContentType.objects.get_for_model(wp).id,
        object_id=wp.id).values_list(field, flat=True)
        
        
def get_bg_style(wp):
    """
    Функция получения кортежа с перечнем названий классов css для задания стилей ячеек таблиц
    Прогноза погоды в зависимости от времени дня (datetime) прогноза.
    Значения кортежа - два вида класса w_day и w_night для отображения "дневных" и "ночных" ячеек
    соответсвенно.
    :param wp: id объекта WeatherProvider, для которого получаем данные
    """
    global BG_STYLE

    forecast_times = list_field_values(wp, 'datetime')
    BG_STYLE = tuple(('w_day' if 8 < t.hour <= 20 else 'w_night' for t in forecast_times))


def get_clouds(wp):
    """
    Функция, возвращающая кортеж с данными об обланчости, включая название соответствующего
    облачности файл PNG.

    :param wp: id объекта WeatherProvider, для которого получаем данные
    :returns: список кортежей, вида [(<файл png>, <облачность в %> <описание>, <класс css>), ...]
    """

    clouds = list_field_values(wp, 'clouds')
    cloud_imgs = list_field_values(wp, 'clouds_img')
    cloud_ranges = (CLOUDS_RANGE[i[2]] if i != 'na' else u'Нет данных' for i in cloud_imgs)

    return zip(cloud_imgs, clouds, cloud_ranges, BG_STYLE)


def get_precipitation(wp):
    """
    Функция, возвращающая кортеж с данными об осадках, включая название соответствующего
    количеству осадков файл PNG.

    :param wp: id объекта WeatherProvider, для которого получаем данные
    :returns: список кортежей, вида [(<файл png>, <кол-во выпавших осадков>, <описание>, <класс css>), ...]
    """

    precipitation = list_field_values(wp, 'precipitation')
    falls_imgs = list_field_values(wp, 'falls_img')
    falls_ranges = (FALLS_RANGE[i] for i in falls_imgs)

    return zip(falls_imgs, precipitation, falls_ranges, BG_STYLE)


def get_wind(wp):
    """
    Функция, возвращающая кортеж с данными о ветре для определенного погодного API.

    :param wp: id объекта WeatherProvider, для которого получаем данные
    :returns: список кортежей, вида [(<скорость ветра>, <направление ветра в градусах>, <класс css>), ...]
    """

    wind_speeds = list_field_values(wp, 'wind_speed')
    wind_directions = list_field_values(wp, 'wind_direction')

    return zip(wind_speeds, wind_directions, BG_STYLE)


def weather(request, current_tab):
    params = {}
    forecast = []

    fields = WeatherValue._meta.fields
    
    # Получаем все модели плагинов типа 'Forecast'
    f_objs = get_plugins('Forecast')

    # Для каждой модели типа 'Forecast' получаем список подключенных объектов (is_used=True),
    # учавствующих в усреднении (on_sidebar=True) и добавляем их в один кортеж.
    f_objs_used = reduce(lambda res, f: res + tuple(f.objects.filter(
        is_used=True, on_sidebar=True)), f_objs, ())
        

    if f_objs_used:
        # Если хотябы один прогнозный API добавлен, собираем список данных для передачи в шаблон.
        # wp - от Weather Provider
        for wp in f_objs_used:
            # Получаем кортеж названий классов css
            get_bg_style(wp)

            # Если ни одного названия класса css в переменной BG_STYLE не присутствует,
            # считаем, что нет данных для данного прогнозного API и пропускаем данную итерацию.
            if not BG_STYLE:
                continue

            values = []
            for field_i in fields[2:-3]:
                field_values = [field_i.name, field_i.verbose_name, field_i.help_text]

                if field_i.name == 'clouds':
                    field_values.append(get_clouds(wp))
                elif field_i.name == 'precipitation':
                    field_values.append(get_precipitation(wp))
                elif field_i.name == 'wind_speed':
                    field_values.append(get_wind(wp))
                else:
                    field_values.append(zip(list_field_values(wp, field_i.name), BG_STYLE))

                values.append(field_values)

            site = wp.url.split('/')[2].split('.')
            forecast.append((site[-2] + '.' + site[-1], values, wp.city))

        params = {'forecast': forecast}

    return call_template(
        request,
        params,
        current_tab=current_tab
    )
