# coding=utf-8
from django.contrib.sessions.models import Session

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

    two_week_events = get_events(14)
    params = {'active_app_name': 'events', 'events_list': two_week_events}

    request.session.save()
    current_session = request.session.session_key

    if two_week_events:
        new_events = two_week_events.exclude(session_keys__session_key=current_session)
        for event in new_events:
            event.session_keys.add(Session.objects.get(pk=current_session))

    return call_template(request, params)
