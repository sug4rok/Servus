﻿# coding=utf-8
from django.conf.urls import patterns, include, url
from .settings import MEDIA_ROOT
from base.models import Application
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'home.views.home', {'current_tab':'home'}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':MEDIA_ROOT}),
    url(r'^slideshow/$', 'slideshow.views.slideshow'),
    url(r'^slide/$', 'slideshow.views.slide'),
    url(r'^amount_events/$', 'events.views.amount_events'),
    url(r'^summary/$', 'home.views.summary'),
    url(r'^admin/', include(admin.site.urls)),
)

for app in Application.objects.filter(is_tab=1).values_list('name', flat=True):
    urlpatterns += patterns(app + '.views',
                            url(r'^%s/$' % app, app, {'current_tab': '%s' % app}),
                            )
