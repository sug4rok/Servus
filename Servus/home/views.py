# -*- coding: utf_8 -*-
from base.views import call_template, Events, get_alert

def home(request, current_tab): 
    pn, pv = [], []
    
    try:
        events = Events.objects.filter(event_viewed=0)
        events_data = []
        if len(events):
            for event in events:
                events_data.append((
                    get_alert(event.event_imp), 
                    event.event_datetime,
                    event.event_src,
                    event.event_descr
                ))
            pn.append('events')
            pv.append(events_data)
        else:
            raise Events.DoesNotExist
    except Events.DoesNotExist:
        pass      

    return call_template(
        request,
        param_names = pn,
        param_vals = pv,
        current_tab=current_tab
    )