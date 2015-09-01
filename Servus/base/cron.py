# coding=utf-8
from datetime import datetime, timedelta
from base.utils import CJB
from django_cron.models import CronJobLog
from events.models import Event
from climate.models import TempHumidValue


class DelOutdatedDCLogs(CJB):
    """
    Удаление устаревший логов django-cron
    """

    RUN_AT_TIMES = ['05:00', ]

    def do(self):
        try:
            CronJobLog.objects.filter(end_time__lte=datetime.today() - timedelta(days=32)).delete()
        except CronJobLog.DoesNotExist:
            pass


class DelOutdatedTHData(CJB):
    """
    Удаление устаревший данных температуры и влажности
    """

    RUN_AT_TIMES = ['05:00', ]

    def do(self):
        try:
            TempHumidValue.objects.filter(datetime__lte=datetime.today() - timedelta(days=15)).delete()
        except TempHumidValue.DoesNotExist:
            pass


class DelOutdatedEvents(CJB):
    """
    Удаление устаревший событий
    """

    RUN_AT_TIMES = ['05:00', ]

    def do(self):
        try:
            Event.objects.filter(datetime__lte=datetime.today() - timedelta(days=32)).delete()
        except Event.DoesNotExist:
            pass
