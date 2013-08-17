from base.views import *
from weather.models import RP5RU

def weather(request):
    active_app_name = os.path.dirname(os.path.relpath(__file__))
    get_tab_options(active_app_name)
    params['rp5ru']=RP5RU.objects.all()
    return render_to_response('weather/tab.html', params)