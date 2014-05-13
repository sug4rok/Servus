﻿# Django settings for Servus project.
# coding=utf-8

SITE_NAME = 'Servus'
SPEAKER_NAME = 'Servus'

# Folder that contains photo albums for slideshow
SLIDESHOW_ROOT = 'static/img/slideshow'

# Plans of house to display on the main page
# (should be placed in a "static/img/home" directory).
HOUSE_PLANS = (
    ('Вид с севера', 'plan1.png'),
)

# Arduino COM port number
PORT = 7