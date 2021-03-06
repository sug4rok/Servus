# coding=utf-8
from datetime import datetime, timedelta

from base.settings import INSTALLED_APPS
from .models import Event


def get_events(days):
    """
    События за последние days дней.

    :param days: int Количество дней, за которые нужно вывести произошедшие события.
    :returns: list Непросмотренные пользователем события за последнии days дней.
    """

    try:
        events = Event.objects.filter(datetime__gte=datetime.now() - timedelta(days=days)).order_by(
            '-datetime')
        return events
    except Event.DoesNotExist:
        return []


def event_setter(source, message, level, delay=24, sms=False, email=False):
    """
    Функция записи новых сообщений в БД (таблица base_event).
    В БД записываются только уникальные (сравнение message) в пределах семи дней сообщения.

    :param source: str Источник события.
    :param message: str Описание события (сообщение).
    :param level: int Код уровня критичности события от 0 до 4.
    Варианты: 0 - 'default', 1 - 'success', 2 - 'info', 3 - 'warning', 4 - 'danger'.
    :param delay: int Ннтервал добавления (в часах) аналогичной записи о событии.
    :param sms: bool Необходимость отправки SMS-сообщения.
    :param email: bool Необходимость отправки EMail-сообщения.
    Во время записи в БД меняем sms_sent и email_sent на противоположное значение, эти параметры меняют свой
    смысл с "отправлять"/"не отправлять" на "отправлено/не отправлено". Пример: параметр sms=False - означает
    не отправлять СМС о событии, в базу попадет событие со значением в поле sms_sent = True - отправлено,
    значит cron это событие пропустит и не отправит СМС, что нам и нужно.
    """

    events = Event.objects.filter(datetime__gte=datetime.now() - timedelta(hours=delay))

    if message not in events.values_list('message', flat=True):

        if source not in INSTALLED_APPS:
            source = 'system'

        Event.objects.create(source=source, message=message, level=level, sms_sent=not sms, email_sent=not email)
