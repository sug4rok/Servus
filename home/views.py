import os
from Servus.settings import STATIC_URL
from base.views import call_template

path_to_img = os.path.join(STATIC_URL, 'img/home')

params = {}
def home(request, current_tab):   
    pn, pv = [], []
    
    print path_to_img
    return call_template(
        request,
        param_names = pn,
        param_vals = pv,
        current_tab=current_tab
    )