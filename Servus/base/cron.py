# coding=utf-8
from datetime import datetime, timedelta

from django_cron.models import CronJobLog

from base.utils import CJB
from events.models import Event
from climate.models import TempHumidValue


class DelOutdatedDCLogs(CJB):
    """Удаление устаревший логов django-cron"""

    RUN_AT_TIMES = ['05:00', ]

    def do(self):
        CronJobLog.objects.filter(end_time__lte=datetime.today() - timedelta(days=32)).delete()


class DelOutdatedTHData(CJB):
    """Удаление устаревший данных температуры и влажности"""

    RUN_AT_TIMES = ['05:00', ]

    def do(self):
        TempHumidValue.objects.filter(datetime__lte=datetime.today() - timedelta(days=15)).delete()


class DelOutdatedEvents(CJB):
    """Удаление устаревший событий"""

    RUN_AT_TIMES = ['05:00', ]

    def do(self):
        Event.objects.filter(datetime__lte=datetime.today() - timedelta(days=32)).delete()
