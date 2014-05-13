# coding=utf-8
from datetime import datetime, timedelta
from django_cron import CronJobBase, Schedule
from base.models import Event


def event_setter(event_src, event_descr, event_imp):
    """
    Функция записи новых сообщений в БД (таблица base_event).
    В БД записываются только уникальные (сравнение event_descr) в пределах семи дней сообщения.

    :param event_src: источник события
    :param event_descr: описание события (сообщение)
    :param event_imp: важность (от 0 до 4)
    """

    if event_imp == 4:
        td = timedelta(hours=1)
    elif event_imp ==3:
        td = timedelta(hours=3)
    else:
        td = timedelta(days=1)

    events = Event.objects.filter(event_datetime__gte=datetime.now() - td)

    if event_descr not in events.values_list('event_descr', flat=True):
        Event.objects.create(event_src=event_src, event_descr=event_descr, event_imp=event_imp)


class CJB(CronJobBase):
    """
    Промежуточный CronJobBase класс (см. https://github.com/Tivix/django-cro),
    наследуемый классами в cron.py.
    """

    RUN_EVERY_MINS = 0
    RUN_AT_TIMES = []

    if RUN_EVERY_MINS:
        schedule = Schedule(
            retry_after_failure_mins=5,
            run_at_times=RUN_EVERY_MINS
        )
    elif RUN_AT_TIMES:
        schedule = Schedule(
            retry_after_failure_mins=5,
            run_every_mins=RUN_AT_TIMES
        )
    else:
        schedule = Schedule(
            retry_after_failure_mins=5,
            run_every_mins=15
        )

    def __init__(self):
        self.code = type(self).__name__
