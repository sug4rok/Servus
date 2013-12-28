# -*- coding: utf_8 -*-
from django.http import HttpResponseRedirect
from django.contrib.sessions.models import Session
from base.views import call_template, get_alert, get_events
from base.models import Event


def home(request, current_tab):
    current_session = request.session.session_key

    # Получение списка событий для текущей сессии.
    # Если с событием еще не ассоциирован ключ данной сессии, оно добавляется в список events.
    events = get_events(current_session)
    events_data = []

    if len(events):
        for event in events:
            events_data.append((
                event.id,
                get_alert(event.event_imp), 
                event.event_datetime,
                event.event_src,
                event.event_descr
            ))

    params = {'events': events_data}

    # Обработка нажатия кнопки "x" на определнном событии.
    # (Ассоциируем с данным событием определенный ключ сессии).
    if request.method == 'POST':
        event_id = request.POST.get('event_id', '')
        if event_id:
            Event.objects.get(id=event_id).session_keys.add(Session.objects.get(pk=current_session))
            return HttpResponseRedirect('/%s/' % current_tab)

    return call_template(
        request,
        params,
        current_tab=current_tab
    )