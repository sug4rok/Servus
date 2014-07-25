# coding=utf-8
from django.conf.urls import patterns, include, url
from settings import MEDIA_ROOT
from base.models import Tab
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'home.views.home', {'current_tab': 'home'}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    url(r'^slideshow/$', 'slideshow.views.slideshow'),
    url(r'^slide/$', 'slideshow.views.slide'),
    url(r'^amount_events/$', 'events.views.amount_events'),
    url(r'^summary/$', 'home.views.summary'),
    url(r'^admin/', include(admin.site.urls)),
)

for tab_app in Tab.objects.filter(is_shown=1).values_list('app_name', flat=True):
    urlpatterns += patterns(tab_app+'.views',
        url(r'^%s/$' % tab_app, tab_app, {'current_tab':'%s' % tab_app}),
    )