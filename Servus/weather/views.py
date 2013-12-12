# coding=utf-8
from base.views import call_template, get_weekday, get_month
from weather.models import Weather, WeatherProvider

CLOUDS_RANGE = {
    '0': 'Ясно',
    '1': 'Малооблачно',
    '2': 'Переменная облачность',
    '3': 'Облачно с прояснениями',
    '4': 'Облачно',
    '5': 'Пасмурная погода',
    'na': 'Нет данных'
}
FALLS_RANGE = {
    't0d0': 'Без осадков',
    't1d0': 'Кратковременный дождь',
    't1d1': 'Небольшой дождь',
    't1d2': 'Дождь',
    't1d3': 'Сильный дождь',
    't1d4': 'Ливень',
    't1d5': 'Гроза',
    't2d0': 'Кратковременный мокрый снег',
    't2d1': 'Небольшой мокрый снег',
    't2d2': 'Мокрый снег',
    't2d3': 'Сильный мокрый снег',
    't2d4': 'Метель',
    't3d0': 'Кратковременный снег',
    't3d1': 'Небольшой снег',
    't3d2': 'Снег',
    't3d3': 'Сильный снег',
    't3d4': 'Метель',
    'na': 'Нет данных'
}
WEATHER_PROVIDERS = {
    'rp5': 'rp5.ru',
    'wua': 'weather.ua',
    'ya': 'Яндекс.Погода',
    'owm': 'Open Weather Map'
}


def weather(request, current_tab):
    pn, pv = [], []

    def list_field_values(wp, field):
        """
        Функция получения данных из базы для определенного прогнозного API и указанного поля
        На входе: 
            - id объекта WeatherProvider, для которого получаем данные
            - поле таблицы базы данных, например 'clouds'
        На выходе: список даанных указанного поля
        """

        return Weather.objects.filter(wp=wp).values_list(field, flat=True)

    def get_field_data(wp, field, measure):
        """
        Базовая функция, возвращающая набор данных в определенном порядке для шаблона weather/tab.html
        На входе:
            - id объекта WeatherProvider, для которого получаем данные
            - поле таблицы базы данных, например 'temperature'
            - еденица измерения
        На выходе: кортеж, вида (<имя поля>, <описание>, <ед. измерения>, [(список значений поля]))
        """

        return (
            field.name,
            field.verbose_name,
            measure,
            list_field_values(wp, field.name)
        )

    def get_forecast_time(wp):
        """
        Функция, возвращающая кортеж с данными о времени для определенного погодного API.
        На входе: id объекта WeatherProvider, для которого получаем данные
        На выходе: кортеж, вида (<день недели>, <день> <месяц>, <час:00>)
        """

        forecast_times = []
        for forecast_time in list_field_values(wp, 'datetime'):
            forecast_times.append((
                get_weekday(forecast_time.weekday()),
                '%s %s' % (forecast_time.day, get_month(forecast_time.month)),
                '%s: 00' % str(forecast_time.hour)
            ))
        return forecast_times

    def get_clouds(wp):
        """
        Функция, возвращающая кортеж с данными об обланчости, включая название соответствующего
        облачности файл PNG.
        На входе: id объекта WeatherProvider, для которого получаем данные
        На выходе: кортеж, вида (<файл png>, <облачность в %> <описание>, <время суток>)
        , где <время суток> - 'd' или 'n' (соответсвенно день, или ночь), используется для
        затемнения "ночных" ячеек таблицы.
        """

        clouds_data = []
        clouds = list_field_values(wp, 'clouds')
        for num, clouds_img in enumerate(list_field_values(wp,'clouds_img')):
            if clouds_img != 'na':
                clouds_data.append((clouds_img + '.png', clouds[num], CLOUDS_RANGE[clouds_img[2]], clouds_img[1]))
            else:
                clouds_data.append((clouds_img + '.png', clouds[num], CLOUDS_RANGE[clouds_img], 'd'))
        return clouds_data

    def get_precipitation(wp):
        """
        Функция, возвращающая кортеж с данными об осадках, включая название соответствующего
        количеству осадков файл PNG.
        На входе: id объекта WeatherProvider, для которого получаем данные
        На выходе: кортеж, вида (<файл png>, <количество выпавших осадков в мм>, <описание>, <время суток>)
        , где <время суток> - 'd' или 'n' (соответсвенно день, или ночь), используется для
        затемнения "ночных" ячеек таблицы.
        """

        precipitation_data = []
        precipitation = list_field_values(wp, 'precipitation')
        clouds_img = list_field_values(wp,'clouds_img')
        for num, falls_img in enumerate(list_field_values(wp, 'falls_img')):
            if falls_img != 'na':
                precipitation_data.append((falls_img + '.png', precipitation[num], FALLS_RANGE[falls_img], clouds_img[num][1]))
            else:
                precipitation_data.append((falls_img + '.png', precipitation[num], FALLS_RANGE[falls_img], 'd'))
        return precipitation_data

    def get_wind(wp):
        """
        Функция, возвращающая кортеж с данными о ветре для определенного погодного API.
        На входе: id объекта WeatherProvider, для которого получаем данные
        На выходе: кортеж, вида (<скорость ветра>, <направление ветра в градусах>)
        """

        wind_data = []
        wind_speed = list_field_values(wp, 'wind_speed')
        for num, wind_direction in enumerate(list_field_values(wp, 'wind_direction')):
            wind_data.append((wind_speed[num], wind_direction))
        return wind_data

    forecast = []
    fields = Weather._meta.fields

    wps = ((wp.id, wp.weather_provider, wp.weather_city) for wp in WeatherProvider.objects.all())
    if wps:
        # Если хотябы один прогнозный API добавлен, собираем список данных для передачи в шаблон.
        for wp in wps:
            value_set = []
            for field in fields[2:-3]:
                if field.name == 'datetime':
                    value_set.append((field.name, field.verbose_name, '', get_forecast_time(wp[0])))
                elif field.name == 'clouds':
                    value_set.append((field.name, field.verbose_name, '', get_clouds(wp[0])))
                elif field.name == 'precipitation':
                    value_set.append((field.name, field.verbose_name, '', get_precipitation(wp[0])))
                elif field.name == 'temperature':
                    value_set.append(get_field_data(wp[0], field, '°C'))
                elif field.name == 'pressure':
                    value_set.append(get_field_data(wp[0], field, 'мм рт. ст.'))
                elif field.name == 'humidity':
                    value_set.append(get_field_data(wp[0], field, '%'))
                elif field.name == 'wind_speed':
                    value_set.append((field.name, field.verbose_name, 'м/c', get_wind(wp[0])))
            forecast.append((WEATHER_PROVIDERS[str([1])], value_set, wp[2]))

        pn.append('forecast')
        pv.append(forecast)

    return call_template(
        request,
        param_names = pn,
        param_vals = pv,
        current_tab=current_tab
    )