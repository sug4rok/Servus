# coding=utf-8
from django_cron import CronJobBase, Schedule


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
