# coding=utf-8
from django.conf.urls import patterns, include, url
from base.models import Tab
from base.views import main_page, slideshow, events

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', main_page),
    url(r'^slideshow/$', slideshow),
    url(r'^events/$', events),
    url(r'^summary/$', 'home.views.summary'),
    url(r'^admin/', include(admin.site.urls)),
)

for tab_app in Tab.objects.filter(is_shown=1).values_list('app_name', flat=True):
    urlpatterns += patterns(tab_app+'.views',
        url(r'^%s/$' % tab_app, tab_app, {'current_tab':'%s' % tab_app}),
    )