# coding=utf-8
from base.utils import CJB
from plugins.utils import get_used_plugins_by
from .models import WeatherValue
from .utils import get_weather


class GetWeatherJob(CJB):
    """
    CronJobBase класс для получения прогноза погоды
    """

    RUN_EVERY_MINS = 60

    @staticmethod
    def do():
        """
        Метод для опроса всех прогнозных провайдеров (подключенные плагины прогноза погоды)
        и запись полученных результатов с помощью функции weather_setter в таблицу БД Weather.
        """

        forecasts = get_used_plugins_by(plugin_type='Forecast')

        if forecasts:
            # Очищаем базу weather_weather перед заполнением свежими данными
            WeatherValue.objects.all().delete()

            for wp in forecasts:
                get_weather(wp)
