﻿# coding=utf-8
import os
from sys import platform
from locale import setlocale, LC_ALL

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ky-kr37p8k^qdos0dk(ijv9m%*8(zre2+s@yct%+w(2(z1$2h2'

DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_cron',
    'base',
    'slideshow',
    'plugins',
)

# Containers - applications for plug-ins of the Servus
CONTAINER_APPS = (
    'system',  # System application. Don't delete it!
    'home',  # System application. Don't delete it!
    'events',  # System application. Don't delete it!
    'climate',
    'weather',
)

PLUGINS = (
    # 'plugins.user_sms_ru',  # Sending sms through the website sms.ru
    'plugins.arduino',  # Arduino controller
    # 'plugins.arduino_bh1750',  # for connecting a BH1750 sensors (ambient light measurement) to the Arduino
    # 'plugins.arduino_bmp085',  # for connecting a BMP085/BMP180 sensor to the Arduino
    # 'plugins.arduino_dht',  # for connecting a DHT sensor (DHT11, DHT22) to the Arduino
    # 'plugins.arduino_ds18d20',  # for connecting a DS18D20 sensor to the Arduino
    'plugins.arduino_on_off_switch',  # on/off switch states
    # 'plugins.arduino_reed_switch',  # reed switch sensors
    # 'plugins.arduino_yl83',  # for connecting a YL-83 raindrop sensors
    # 'plugins.weather_openweathermap',  # weather forecast from openweathermap.org
    # 'plugins.weather_weather_ua',  # weather from weather.ua
    # 'plugins.system_hddtemp',  # temperature HDD in linux (need to install hddtemp)
    'plugins.system_ip_online',  # ping utility
    'plugins.system_mac_online',  # search for device mac address in the home network
)

INSTALLED_APPS += (PLUGINS + CONTAINER_APPS)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/plugins/{0}/tempates/'.format(p.split('.')[1]) for p in PLUGINS],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
            ],
            'debug': False,
        },
    },
]

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

WSGI_APPLICATION = 'base.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'NAME': 'servusdb',
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
CONN_MAX_AGE = 60

if 'win' in platform:
    OS = 'windows'
    LOCALE = 'Russian'
elif 'linux' in platform:
    OS = 'linux'
    LOCALE = 'ru_RU.utf8'
else:
    OS = 'unknown'
    LOCALE = ''

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-RU'
setlocale(LC_ALL, LOCALE)
USE_I18N = True
USE_L10N = True
USE_TZ = False

# =================== #
#   Servus settings   #
# =================== #
SITE_NAME = 'Servus'

# Bootstrap theme (dark or light)
THEME = 'dark'

ALERTS = {0: 'default', 1: 'success', 2: 'info', 3: 'warning', 4: 'danger'}

# Настройки почтового аккаунта gmail для отправки писем
# Запуск эмулятора почтового сервера: python -m smtpd -n -c DebuggingServer localhost:587
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'localhost'  # 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'user@gmail.com'
# EMAIL_HOST_PASSWORD = 'password'

# Cookies settings
SESSION_COOKIE_NAME = 'Servus_sessionid'
SESSION_COOKIE_AGE = 99999999

# Tasks for django-cron
CRON_CLASSES = [
    'django_cron.cron.FailedRunsNotificationCronJob',
    'base.cron.DelOutdatedEvents',
    'slideshow.cron.SlideshowJob',
    # 'events.cron.EmailsSendJob',
    # 'events.cron.SMSSendJob',
    # 'system.cron.PerfomArduinoCommands',
    # 'home.cron.GetOnOffSwitchState',
    # 'climate.cron.GetAmbientLightData',
    # 'climate.cron.GetPressureData',
    # 'climate.cron.GetRaindropData',
    # 'climate.cron.GetTempHumidData',
    # 'weather.cron.GetWeatherJob',
    # 'plugins.system_hddtemp.cron.GetHDDTemp',
    # 'plugins.system_ip_online.cron.GetIPOnline',
    # 'plugins.system_mac_online.cron.GetMACOnline',
]

DJANGO_CRON_DELETE_LOGS_OLDER_THAN = 32

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'main_formatter': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:\n'
                      'Message: %(message)s\n'
                      'Path: %(pathname)s:%(lineno)d in function: %(funcName)s\n',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'production_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/product.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_false'],
        },
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 7,
            'formatter': 'main_formatter',
            'filters': ['require_debug_true'],
        },
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null', ],
        },
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'py.warnings': {
            'handlers': ['null', ],
        },
        '': {
            'handlers': ['console', 'production_file', 'debug_file'],
            'level': 'DEBUG',
        },
    }
}
