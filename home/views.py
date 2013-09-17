from base.views import call_template

params = {}
def home(request, current_tab):   
    if not params:
        return call_template(request, current_tab=current_tab)
    else:
        return call_template(request, params, current_tab=current_tab)