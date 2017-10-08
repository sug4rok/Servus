# coding=utf-8
from django.contrib.sessions.models import Session

from base.views import call_template
from .utils import get_events
from .models import Event


def events(request):
    """
    Вывод событий последних days дней на вкладку События. При нажатии на кнопку все еще не
    ассоциированные с данной сессией браузера события добавятся в таблицу events_event_session_keys
    и будут считаться просмотренными.

    :param request: django request
    """

    days = 14
    params = {'active_app_name': 'events', 'events_list': get_events(days)}

    request.session.save()
    current_session = request.session.session_key

    new_events = Event.objects.all().exclude(session_keys__session_key=current_session)
    for event in new_events:
        event.session_keys.add(Session.objects.get(pk=current_session))

    return call_template(request, params)
