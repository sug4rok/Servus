# coding=utf-8
from django_cron import CronJobBase, Schedule


class CJB(CronJobBase):
    """
    Промежуточный CronJobBase класс (см. https://github.com/Tivix/django-cron),
    наследуемый классами в cron.py.
    """

    RUN_EVERY_MINS, RUN_AT_TIMES, code = (None, None, None)
    MIN_NUM_FAILURES = 10
    # FAILED_RUNS_CRONJOB_EMAILS_PREFIX = 'Ошибка выполнения задания: '
    ALLOW_PARALLEL_RUNS = True
    schedule = Schedule(
        # retry_after_failure_mins=5,
        run_every_mins=15
    )

    def __init__(self):
        super(CJB, self).__init__()
        if self.RUN_EVERY_MINS:
            self.schedule = Schedule(run_every_mins=self.RUN_EVERY_MINS)
        elif self.RUN_AT_TIMES:
            self.schedule = Schedule(run_at_times=self.RUN_AT_TIMES)
        self.code = type(self).__name__
