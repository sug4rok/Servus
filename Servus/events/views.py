# coding=utf-8
from django.contrib.sessions.models import Session
from django.db import IntegrityError

from base.views import call_template
from .utils import get_events
from .models import Event


def events(request):
    """
    Вывод событий последних двух недель на вкладку События. При нажатии на кнопку все еще не
    ассоциированные с данной сессией браузера события добавятся в таблицу events_event_session_keys
    и будут считаться просмотренными.

    :param request: django request
    """

    return call_template(request, {'active_app_name': 'events', 'events_list': get_events(14)})


def set_viewed_events(request):
    two_week_events = get_events(14)

    request.session.save()
    current_session = request.session.session_key

    if two_week_events.count():
        new_events = two_week_events.exclude(session_keys__session_key=current_session)
        if new_events.count():
            so = Session.objects.get(pk=current_session)
            for event in new_events:
                try:
                    event.session_keys.add(so)
                except IntegrityError:
                    continue

    return call_template(request, {})
