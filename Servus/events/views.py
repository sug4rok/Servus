# coding=utf-8
from django.contrib.sessions.models import Session

from base.views import call_template
from .utils import get_events, ALERTS
from .models import Event


def events(request):
    """
    Вывод событий последних days дней на вкладку События. При нажатии на кнопку все еще не
    ассоциированные с данной сессией браузера события добавятся в таблицу events_event_session_keys
    и будут считаться просмотренными.

    :param request: django request
    """

    days = 14
    params = {'active_app_name': 'events', 'events': get_events(days), 'alerts': ALERTS}
    
    request.session.save()
    current_session = request.session.session_key

    if request.POST.get('events'):
        events = Event.objects.all().exclude(session_keys__session_key=current_session)
        for e in events:
            e.session_keys.add(Session.objects.get(pk=current_session))

    return call_template(request, params)
