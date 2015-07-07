# coding=utf-8
from base.utils import CJB
from .models import WeatherProvider
from .weather_getter import get_weather
from .weather_setter import *


class GetWeatherJob(CJB):
    """
    CronJobBase класс для получения прогноза погоды
    """

    RUN_EVERY_MINS = 60

    @staticmethod
    def do():
        """
        Метод для опроса всех прогнозных провайдеров (таблица БД WeatherProvider)
        и запись полученных результатов с помощью функции weather_setter в таблицу БД Weather.
        """

        wps = WeatherProvider.objects.filter(is_used=True)
        if wps.count():
            weather_db_cleaner()
            for wp in wps:
                weather_setter(get_weather(wp))
