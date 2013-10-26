# -*- coding: utf_8 -*-
from django.http import HttpResponseRedirect
from base.views import call_template, get_alert, get_remote_hash, get_events
from base.models import Event, RemoteHost

def home(request, current_tab):

    pn, pv = [], []
    
    # Расчет хеша для текущего браузера и IP-адреса.
    # Необходимо для выведения списка событий для тех, кто еще не просмотрел их.
    r_hash, last_access = get_remote_hash(request)
    
    # Получение списка событий для расчитанного ранее хеша.
    # Если с событием не еще не ассоциирован данный хеш, оно добавляется в список events.
    events = get_events(r_hash)
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
    pn.append('events')
    pv.append(events_data)

    # Обработка нажатия кнопки "x" на определнном событии.
    # (Ассоциируем с данным событием определенный хеш).
    if request.method == 'POST':
        event_id = request.POST.get('event_id', '')
        if event_id :
            Event.objects.get(id=event_id).r_hashes.add(RemoteHost.objects.get(r_hash=r_hash))
            return HttpResponseRedirect('/%s/' % current_tab)		

    return call_template(
        request,
        param_names = pn,
        param_vals = pv,
        current_tab=current_tab
    )
