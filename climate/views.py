﻿from base.views import call_template

params = {}
def climate(request, current_tab): 
    pn, pv = [], []

    return call_template(
        request,
        param_names = pn,
        param_vals = pv,
        current_tab=current_tab
    )