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