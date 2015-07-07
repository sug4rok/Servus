# coding=utf-8
from datetime import datetime, timedelta
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
    :reuturns: список кортежей, вида [(<скорость ветра>, <направление ветра в градусах>, <класс css>), ...]
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

        params = {'forecast':forecast}

    return call_template(
        request,
        params,
        current_tab=current_tab
    )


def nearest_forecast(day):
    """
    Функция получения некоторых усредненных данных прогноза погоды для активированных погодных API,
    отображаемых на Главной странице.
    :param day: день ('сегодня' | 'завтра'), для которого будем усреднять прогноз.
    :returns: словарь, с данными о температуре, скорости ветра и соответствующим облачности и
    осадкам файлам PNG.
    """

    if day == 'сегодня':
        d = datetime.today()
    else:
        d = datetime.today() + timedelta(days=1)

    # Создаем список объектов Weather, всех активированных прогнозных API,
    # приходящихся на переданный в функциию день с 12:00 до 16:00 включительно
    # (будем считать, что день у нас с 12 до 16 часов ;)).
    dt1 = datetime(d.year, d.month, d.day, 12)
    dt2 = datetime(d.year, d.month, d.day, 16)
    w_objs = Weather.objects.filter(wp__on_sidebar=True, wp__is_used=True, datetime__range=[dt1, dt2])

    amount_data = len(w_objs)
    if amount_data:
        forecast = {
            'temperature': w_objs.values_list('temperature', flat=True),
            'wind_speed': w_objs.values_list('wind_speed', flat=True),
            'clouds_img': w_objs.values_list('clouds_img', flat=True),
            'falls_img': w_objs.values_list('falls_img', flat=True),
            'wind_direction': w_objs.values_list('wind_direction', flat=True),
        }
    else:
        return None

    # Заполняем словарь forecast снова, теперь уже усредненными данными
    temperature = round(float(sum(forecast['temperature'])) / amount_data, 0)
    for f_k, f_v in forecast.iteritems():
        if f_k == 'falls_img':
            tmp_data1 = sum([float(f[1]) for f in f_v]) / amount_data

            if tmp_data1 > 0.5:
                if temperature > 2:
                    tmp_data1 = '1'
                elif temperature < 0:
                    tmp_data1 = '3'
                else:
                    tmp_data1 = '2'
                tmp_data2 = sum([float(f[3]) for f in f_v]) / amount_data
            else:
                tmp_data1, tmp_data2 = '0', 0.0

            file_img = 't%sd%.0f' % (tmp_data1, tmp_data2)
            forecast[f_k] = [(file_img, FALLS_RANGE[file_img])]
        elif f_k == 'clouds_img':
            tmp_data1 = sum([float(f[2]) for f in f_v]) / amount_data
            file_img = 'cd%.0f' % tmp_data1
            forecast[f_k] = [(file_img, CLOUDS_RANGE[file_img[2]])]
        elif f_k == 'temperature':
            forecast[f_k] = '%d' % temperature
        else:
            forecast[f_k] = '%d' % round(float(sum(f_v)) / amount_data, 0)
    forecast['day'] = day
    return forecast


def widget():
    """
    Функция для получения данных для отображение краткой сводки прогноза погоды на сегодня и завтра
    на Главной странице
    :return: list Погодные данные
    """

    return (nearest_forecast('сегодня'), nearest_forecast('завтра'))
