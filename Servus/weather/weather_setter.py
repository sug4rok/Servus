from weather.models import Weather

def weather_db_cleaner():
    """
    Очистка базы weather_weather перед заполнением свежими данными
    """
    try:
        Weather.objects.all().delete()
    except Weather.DoesNotExist:
        pass

def weather_setter(weather_data):
    """
    Функция записи массива данных, полученных с помощью функции weather_getter в таблицу weather_weather БД.
    На входе: список с данными, вида [{a1:b1, c1:d1}, {a2:b2, c2:d2},.. {an:bn, cn:dn}]
    """
    for weather in weather_data:
        obj_wp = Weather.objects.create(wp=weather['wp'])
        obj_wp.datetime = weather['datetime']
        if 'clouds' in weather:
            obj_wp.clouds = int(weather['clouds'])
        if 'precipitation' in weather:
            obj_wp.precipitation = float(weather['precipitation'])
        obj_wp.temperature = int(weather['temperature'])
        obj_wp.pressure = int(weather['pressure'])
        obj_wp.humidity = int(weather['humidity'])
        obj_wp.wind_speed = int(weather['wind_speed'])
        obj_wp.wind_direction = int(weather['wind_direction'])
        obj_wp.clouds_img = weather['clouds_img']
        obj_wp.falls_img = weather['falls_img']
        obj_wp.save()