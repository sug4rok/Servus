from base.views import *

def home(request):   
    active_app_name = os.path.dirname(os.path.relpath(__file__))
    get_tab_options(active_app_name)
    return render_to_response('home/tab.html', params)