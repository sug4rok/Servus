from base.views import *
from weather.models import RP5RU

def weather(request):
    active_app_name = os.path.dirname(os.path.relpath(__file__))
    get_tab_options(active_app_name)
    
    fields = RP5RU._meta.fields
    rp5ru = [(field.verbose_name, [values for values in RP5RU.objects.values_list(field.name, flat=True)]) for field in fields[1:-4]]
    
    cloud_cover = []
    cloud_ranges = {
                    0:range(0, 11),
                    1:range(11, 21),
                    2:range(21, 31),
                    3:range(31, 51),
                    4:range(51, 71),
                    5:range(71, 81),
                    6:range(81, 91),
                    7:range(91, 100)
                    }
    for num, item in enumerate(RP5RU.objects.values_list('cloud_cover', flat=True)):
        cloud_item = ''
        if num % 2:
            cloud_item = 'cn'
        else:
            cloud_item = 'cd'
        for cloud_range in cloud_ranges:
            if item in cloud_ranges[cloud_range]:
                cloud_cover.append(cloud_item + str(cloud_range))
    rp5ru_clouds = [(fields[-4].verbose_name, cloud_cover)]
    
    params['rp5ru'] = rp5ru
    params['rp5ru_clouds'] = rp5ru_clouds
    return render_to_response('weather/tab.html', params)