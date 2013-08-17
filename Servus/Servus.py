# Django settings for Servus project.
# -*- coding: utf_8 -*-

SITE_NAME = 'Servus'
SPEAKER_NAME = 'Servus'

TAB_APPS = (
    # These is applications will be added to INSTALLED_APPS. Also it's An Application type for tabs.
    'home',
    'weather',
    'climate'
    )
    
CRON_CLASSES = [
    'weather.cron.GetWeatherJob',
]