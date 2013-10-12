from django_cron import CronJobBase, Schedule
from Servus.Servus import WEATHER_PROVIDERS
from weather.weather_getter import weather_getter
from weather.weather_setter import *

class GetWeatherJob(CronJobBase):
    RUN_EVERY_MINS = 60
    RETRY_AFTER_FAILURE_MINS = 5
    #RUN_AT_TIMES = ['00:15', '04:15', '12:15', '16:15']
    
    schedule = Schedule(
        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS,
        #run_at_times=RUN_AT_TIMES
        run_every_mins=RUN_EVERY_MINS
    )
    code = 'GetWeatherJob'    # a unique code

    @staticmethod
    def do():
        if WEATHER_PROVIDERS:
            weather_db_cleaner()
            for wp in WEATHER_PROVIDERS:
                weather_setter(weather_getter(wp), wp)