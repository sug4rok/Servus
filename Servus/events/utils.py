# coding=utf-8
from datetime import datetime, timedelta
from base.settings import INSTALLED_APPS
from .models import Event


def get_alert(level):
    """
    Функция получения названия уровня критичности события по его коду.

    :param level: int Важность события.
    :returns: str Важность события.
    """

    return {0: 'default', 1: 'success', 2: 'info', 3: 'warning', 4: 'danger'}[level]


def get_events(days, session_key=None):
    """
    События за последние days дней для сессий, не ассоциированных еще с данной сессией.
    Ассоциация события с session_key происходит после его закрытия в списке событий на странице home
    
    :param days: int Количество дней, за которые нужно вывести произошедшие события
    :param session_key: Ключ конкретной сессии для браузера пользоватея, зарегистрированной django.
    :returns: list Непросмотренные или не закрытые пользователем события за последнии days дней.
    """

    try:
        events_data = []
        if session_key:
            events = Event.objects.filter(datetime__gte=datetime.now() - timedelta(days=2)) \
                .exclude(session_keys__session_key=session_key).order_by('-level', '-datetime').values()
        else:
            events = Event.objects.filter(datetime__gte=datetime.now() - timedelta(days=days)) \
                .order_by('-datetime').values()

        if len(events):
            for event in events:
                events_data.append((
                    event['id'],
                    event['source'],
                    event['message'],
                    get_alert(event['level']),
                    event['datetime']
                ))
        return events_data

    except Event.DoesNotExist:
        return []


def get_amount_events(days, session_key=None):
    """
    Функция, выводящая количесво событий и их кретичность для определенной сессии.
    (См. описание к функции get_events).

    :param request: django request.
    :returns: dict Словарь с количеством и уровнем важности непросмотренных событий.
    """

    events_short = Event.objects.filter(datetime__gte=datetime.now() - timedelta(days=days)) \
        .exclude(session_keys__session_key=session_key).values_list('level', flat=True)

    amount_events = len(events_short)
    if amount_events:
        return {'amount': amount_events, 'level': get_alert(max(events_short))}
    else:
        return {'amount': 0, 'level': get_alert(0)}


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
