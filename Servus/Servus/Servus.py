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

# Запускаемые планировщиком задания (см. django-cron документацию)
CRON_CLASSES = [
    'base.cron.SlideshowJob',
    'weather.cron.GetWeatherJob',    
]

# Папка с фотоальбомами для слайдшоу
SLIDESHOW_ROOT = 'static/img/slideshow'

# Типы показываемых в слайдшоу файлов
SLIDESHOW_FILE_TYPES = (
    'jpg',
    'jpeg',
)