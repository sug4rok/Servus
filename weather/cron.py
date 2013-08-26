from xml.dom import minidom
import urllib2
from weather.models import RP5RU
from django_cron import CronJobBase, Schedule
from datetime import datetime, timedelta

def weather_getter():
    '''
    Get the weather forecast from rp5.ru API and 
    put it into weather_rp5ru table of Servus's database
    '''  

    url_sock = urllib2.urlopen("http://rp5.ru/xml/7285/00000/ru")
    parsed_xml = minidom.parse(url_sock)      
    
    try:
        RP5RU.objects.get(time_step=60).delete()
    except RP5RU.DoesNotExist:
        pass
    
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    for i in range(1,5):        
        weather_data = {}
        
        for field in RP5RU._meta.fields[1:]:
            if field.name != 'forecast_time':
                point_names = parsed_xml.getElementsByTagName(field.name)
                point_name = point_names[i-1].childNodes[0].nodeValue
                weather_data[field.name] = point_name 
 
        obj_rp5ru, created = RP5RU.objects.get_or_create(time_step=int(weather_data['time_step']))
        obj_rp5ru.forecast_time = today + timedelta(hours=+(int(weather_data['time_step'])+4)) 
        obj_rp5ru.pressure = int(weather_data['pressure'])
        obj_rp5ru.temperature = int(weather_data['temperature'])
        obj_rp5ru.humidity = int(weather_data['humidity'])
        obj_rp5ru.wind_direction = weather_data['wind_direction']
        obj_rp5ru.wind_velocity = int(weather_data['wind_velocity'])
        obj_rp5ru.cloud_cover = int(weather_data['cloud_cover'])
        obj_rp5ru.falls = int(weather_data['falls'])
        obj_rp5ru.precipitation = float(weather_data['precipitation'])
        obj_rp5ru.drops = int(float(weather_data['drops']))
        obj_rp5ru.save()
        
    url_sock.close()

class GetWeatherJob(CronJobBase):
    #RUN_EVERY_MINS = 60
    RETRY_AFTER_FAILURE_MINS = 5
    RUN_AT_TIMES = ['00:15', '04:15', '12:15', '16:15']
    
    schedule = Schedule(
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS,
                        run_at_times=RUN_AT_TIMES
                        )
    code = 'GetWeatherJob'    # a unique code

    def do(self):
        weather_getter()