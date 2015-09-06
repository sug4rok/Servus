# coding=utf-8
from base.utils import CJB
from plugins.models import PLUGIN_MODELS
from .utils import get_weather, weather_db_cleaner


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
        
        forecasts = filter(lambda f: f.TYPE == 'Forecast', PLUGIN_MODELS['weather'])
        forecasts_used = reduce(lambda res, f: res + tuple(f.objects.filter(is_used=True)), forecasts, ())
        
        if forecasts_used:
            weather_db_cleaner()
            for wp in forecasts_used:
                print wp
                # weather_setter(get_weather(wp))
