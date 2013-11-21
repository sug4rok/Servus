# Django settings for Servus project.
# coding=utf-8

SITE_NAME = 'Servus'
SPEAKER_NAME = 'Servus'

# These is applications will be added to INSTALLED_APPS.
# Also it's An Application type for tabs.
TAB_APPS = (
    'home',
    'climate',   
    'weather',
    )
 
 
CRON_CLASSES = [
    'base.cron.SlideshowJob',
    'weather.cron.GetWeatherJob',    
]

    
# Подпапки, которые должны быть пропущены при индексации.
SLIDESHOW_EXCLUDE_DIRS = (
    'dont_index_me',
)

# Типы показываемых в слайдшоу файлов
SLIDESHOW_FILE_TYPES = (
    'jpg',
    'jpeg',
)


# These forecasts will be added to the weather tab    
# Forecasts:
# rp5 - rp5.ru (http://rp5.ru/xml/7285/00000/ru)
# wua - weather.ua (http://xml.weather.co.ua/1.2/forecast/773?dayf=4?lang=ru)
# ya - yandex.ru (http://export.yandex.ru/weather-ng/forecasts/26063.xml)
# owm - openweathermap.org (http://api.openweathermap.org/data/2.5/forecast/daily?q=St.Petersburg&mode=xml&units=metric&cnt=4)
WEATHER_PROVIDERS = {    
    'rp5':'rp5.ru',
    'wua':'weather.ua',
    'ya':'yandex.ru',
    'owm':'openweathermap.org',
    }