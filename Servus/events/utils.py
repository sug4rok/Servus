# coding=utf-8
from datetime import datetime, timedelta
from .models import Event


def get_alert(e_imp):
    """
    Функция получения степени кретичности системного события

    :param e_imp: integer степень кретичности
    """

    e_status = {
        0: 'default',
        1: 'success',
        2: 'info',
        3: 'warning',
        4: 'danger'
    }
    return e_status[e_imp]


def get_events(session_key=None):
    """
    События за последние 7 дней для сессий, не ассоциированных еще с данным событием.
    Ассоциация события с session_key происходит после его закрытия в списке событий на странице home

    :param session_key: ключ конкретной сессии для браузера пользоватея, зарегистрированной django
    :returns: список не просмотренных или не закрытых пользователем событий за последнии 7 дней
    """

    try:
        events_data = []
        if session_key:
            events = Event.objects.filter(event_datetime__gte=datetime.now() - timedelta(days=2))\
                .exclude(session_keys__session_key=session_key).order_by('-event_imp').values()
        else:
            events = Event.objects.filter(event_datetime__gte=datetime.now() - timedelta(days=14))\
                .order_by('-event_datetime').values()

        if len(events):
            for event in events:
                events_data.append((
                    event['id'],
                    event['event_src'],
                    event['event_descr'],
                    get_alert(event['event_imp']),
                    event['event_datetime']
                ))
        return events_data

    except Event.DoesNotExist:
        return []


def get_amount_events(request):
    """
    Функция, выводящая количесво событий и их кретичность для определенной сессии.
    (См. описание к функции get_events).

    :param request: django request
    :returns: кортеж, вида (<количество сбобытий>, <кретичность>)
    """

    request.session.save()
    events_short = Event.objects.filter(event_datetime__gte=datetime.now() - timedelta(days=2))\
        .exclude(session_keys__session_key=request.session.session_key).values_list('event_imp', flat=True)

    amount_events = len(events_short)
    if amount_events:
        return amount_events, get_alert(max(events_short))
    else:
        return 0, 0


def event_setter(event_src, event_descr, event_imp, delay=24, sms=True, email=True):
    """
    Функция записи новых сообщений в БД (таблица base_event).
    В БД записываются только уникальные (сравнение event_descr) в пределах семи дней сообщения.

    :param event_src: источник события
    :param event_descr: описание события (сообщение)
    :param event_imp: важность (от 0 до 4)
    :param delay: интервал добавления (в часах) аналогичной записи о событии
    :param sms: необходимость отправки SMS-сообщения
    :param email: необходимость отправки EMail-сообщения
    """

    events = Event.objects.filter(event_datetime__gte=datetime.now() - timedelta(hours=delay))

    if event_descr not in events.values_list('event_descr', flat=True):
        Event.objects.create(event_src=event_src, event_descr=event_descr, event_imp=event_imp, sms_sent=not sms, email_sent=not email)