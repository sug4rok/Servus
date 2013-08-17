from xml.dom import minidom
import urllib2
from weather.models import RP5RU
from django_cron import CronJobBase, Schedule

def weather_getter():
    len_RP5RU = len(RP5RU.objects.all())
    while (4 - len_RP5RU) > 0:
        obj_rp5ru = RP5RU(
            time_step=0,
            cloud_cover=0,
            precipitation=0,
            pressure=0,
            temperature=0,
            humidity=0,
            wind_direction='',
            wind_velocity=0,
            falls=0,
            drops=0
        )
        obj_rp5ru.save()
        len_RP5RU+=1

    url_sock = urllib2.urlopen("http://rp5.ru/xml/7285/00000/ru")
    parsed_xml = minidom.parse(url_sock)      
    
    for i in range(1,5):        
        weather_data = {}
        
        for field in RP5RU._meta.fields[1:]:
            point_names = parsed_xml.getElementsByTagName(field.name)
            point_name = point_names[i-1].childNodes[0].nodeValue
            weather_data[field.name] = point_name 
        
        obj_rp5ru = RP5RU(
            id=i,
            time_step = weather_data['time_step'],
            cloud_cover = weather_data['cloud_cover'],
            precipitation = weather_data['precipitation'],
            pressure = weather_data['pressure'],
            temperature = weather_data['temperature'],
            humidity = weather_data['humidity'],
            wind_direction = weather_data['wind_direction'],
            wind_velocity = weather_data['wind_velocity'],
            falls = weather_data['falls'],
            drops = weather_data['drops'],
        )
        obj_rp5ru.save()
        
    url_sock.close()

class GetWeatherJob(CronJobBase):
    #RUN_EVERY_MINS = 60
    RETRY_AFTER_FAILURE_MINS = 5
    RUN_AT_TIMES = ['00:15', '04:15', '12:15', '16:15']
    
    schedule = Schedule(retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS, run_at_times=RUN_AT_TIMES)
    code = 'GetWeatherJob'    # a unique code

    def do(self):
        weather_getter()