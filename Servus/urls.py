﻿from django.conf.urls import patterns, include, url
from home.views import home
from climate.views import climate
from weather.views import weather

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Servus.views.home', name='home'),
    # url(r'^Servus/', include('Servus.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$|^home/$', home),
    url(r'^climate/$', climate),
    url(r'^weather/$', weather),
    
    url(r'^admin/', include(admin.site.urls)),
)
