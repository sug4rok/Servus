# coding=utf-8
from base.utils import CJB
from plugins.utils import get_plugins
from .utils import command, weather_db_cleaner


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
        
        forecasts = get_plugins('Forecast')
        forecasts_used = reduce(lambda res, f: res + tuple(f.objects.filter(is_used=True)), forecasts, ())
        
        if forecasts_used:
            weather_db_cleaner()
            for wp in forecasts_used:
                command(wp, write_db=True)
