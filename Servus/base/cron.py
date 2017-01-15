# coding=utf-8
from datetime import datetime, timedelta

from base.utils import CJB
from events.models import Event


class DelOutdatedEvents(CJB):
    """Удаление устаревший событий"""

    RUN_AT_TIMES = ['05:00', ]

    def do(self):
        Event.objects.filter(datetime__lte=datetime.today() - timedelta(days=90)).delete()
