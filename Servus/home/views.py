# -*- coding: utf_8 -*-
from django.http import HttpResponseRedirect
from base.views import call_template, get_alert, get_remote_hash, get_events
from base.models import Events, RemoteHost

def home(request, current_tab):

    pn, pv = [], []
    
    r_hash, last_access = get_remote_hash(request)
    
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

    if request.method == 'POST':
        event_id = request.POST.get('event_id', '')
        
        if event_id :
            Events.objects.get(id=event_id).r_hashes.add(RemoteHost.objects.get(r_hash=r_hash))
            return HttpResponseRedirect('/%s/' % current_tab)		

    return call_template(
        request,
        param_names = pn,
        param_vals = pv,
        current_tab=current_tab
    )
