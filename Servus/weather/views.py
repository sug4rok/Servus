# coding=utf-8
from base.views import call_template
from .models import Weather, WeatherProvider

CLOUDS_RANGE = {
    '0': u'Ясно',
    '1': u'Малооблачно',
    '2': u'Переменная облачность',
    '3': u'Облачно с прояснениями',
    '4': u'Облачно',
    '5': u'Пасмурная погода'
}
FALLS_RANGE = {
    't0d0': u'Без осадков',
    't1d0': u'Кратковременный дождь',
    't1d1': u'Небольшой дождь',
    't1d2': u'Дождь',
    't1d3': u'Сильный дождь',
    't1d4': u'Ливень',
    't1d5': u'Гроза',
    't2d0': u'Кратковременный мокрый снег',
    't2d1': u'Небольшой мокрый снег',
    't2d2': u'Мокрый снег',
    't2d3': u'Сильный мокрый снег',
    't2d4': u'Метель',
    't3d0': u'Кратковременный снег',
    't3d1': u'Небольшой снег',
    't3d2': u'Снег',
    't3d3': u'Сильный снег',
    't3d4': u'Метель',
    'na': u'Нет данных'
}


def get_bg_style(wp):
    """
    Функция получения кортежа с перечнем названий классов css для задания стилей ячеек таблиц
    Прогноза погоды в зависимости от времени дня (datetime) прогноза.
    Значения кортежа - два вида класса w_day и w_night для отображения "дневных" и "ночных" ячеек
    соответсвенно.
    :param wp: id объекта WeatherProvider, для которого получаем данные
    """
    global BG_STYLE

    forecast_times = Weather.objects.filter(wp=wp).values_list('datetime', flat=True)
    BG_STYLE = tuple(('w_day' if 8 < t.hour <= 20 else 'w_night' for t in forecast_times))


def list_field_values(wp, field):
    """
    Функция получения данных из базы для определенного прогнозного API и указанного поля

    :param wp: id объекта WeatherProvider, для которого получаем данные
    :param field: поле таблицы базы данных, например 'clouds'
    :returns: генератор списка данных указанного поля
    """

    return Weather.objects.filter(wp=wp).values_list(field, flat=True)


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

    fields = Weather._meta.fields
    wps = ((wp.id,
            wp.city,
            wp.get_name_display()) for wp in WeatherProvider.objects.filter(is_used=True))
    if wps:
        # Если хотябы один прогнозный API добавлен, собираем список данных для передачи в шаблон.
        for wp_i in wps:
            # Получаем кортеж названий классов css
            get_bg_style(wp_i[0])

            # Если ни одного названия класса css в переменной BG_STYLE не присутствует,
            # считаем, что нет данных для данного прогнозного API и пропускаем данную итерацию.
            if not BG_STYLE:
                continue

            values = []
            for field_i in fields[2:-3]:
                field_values = [field_i.name, field_i.verbose_name, field_i.help_text]

                if field_i.name == 'clouds':
                    field_values.append(get_clouds(wp_i[0]))
                elif field_i.name == 'precipitation':
                    field_values.append(get_precipitation(wp_i[0]))
                elif field_i.name == 'wind_speed':
                    field_values.append(get_wind(wp_i[0]))
                else:
                    field_values.append(zip(list_field_values(wp_i[0], field_i.name), BG_STYLE))

                values.append(field_values)

            forecast.append((wp_i[2], values, wp_i[1]))

        params = {'forecast': forecast}

    return call_template(
        request,
        params,
        current_tab=current_tab
    )
