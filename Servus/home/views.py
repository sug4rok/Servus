# -*- coding: utf_8 -*-
from base.views import call_template, get_alert, get_remote_ip, get_events
from base.models import Events, RemoteIP

def home(request, current_tab): 
    pn, pv = [], []
    
    ip, last_access = get_remote_ip(request) 
    
    events = get_events(ip)
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
        
        print request.POST
        print '--------', event_id
        
        if event_id :
            Events.objects.get(id=event_id).ips.add(RemoteIP.objects.get(ip=ip))
    
    return call_template(
        request,
        param_names = pn,
        param_vals = pv,
        current_tab=current_tab
    )