# coding=utf-8
from django_cron import CronJobBase, Schedule


class CJB(CronJobBase):
    """
    Промежуточный CronJobBase класс (см. https://github.com/Tivix/django-cron),
    наследуемый классами в cron.py.
    """

    RUN_EVERY_MINS, RUN_AT_TIMES, code = (None, None, None)
    # MIN_NUM_FAILURES = 5
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
        

def fill_base_applications(container_apps):
    """
    If in the database there is a table fill the table base_application.
    
    :param container_apps: tuple CONTAINER_APPS from settings file.
    """
    
    from django.db.utils import OperationalError, ProgrammingError
    try:
        from base.models import Application
        for c_app in container_apps:
            app, created = Application.objects.get_or_create(name=c_app)
            if app.name == 'home':
                app.is_tab = True
            if app.tab_name == '':
                app.tab_name = c_app.capitalize()
            app.save()
    except (OperationalError, ProgrammingError):
        pass
