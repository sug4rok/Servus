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


def get_weekday(weekday):
    """
    Функция получения названия дня недели

    :param weekday: порядковый номер дня недели
    """

    days = {
        0: u'Понедельник',
        1: u'Вторник',
        2: u'Среда',
        3: u'Четверг',
        4: u'Пятница',
        5: u'Суббота',
        6: u'Воскресенье'
    }
    return days[weekday]


def get_month(month):
    """
    Функция получения названия месяца в родительном падеже

    :param month: порядковый номер месяца
    """

    days = {
        1: u'Января',
        2: u'Февраля',
        3: u'Марта',
        4: u'Апреля',
        5: u'Мая',
        6: u'Июня',
        7: u'Июля',
        8: u'Августа',
        9: u'Сентября',
        10: u'Октября',
        11: u'Ноября',
        12: u'Декабря'
    }
    return days[month]