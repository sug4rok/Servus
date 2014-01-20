# coding=utf-8
from django.conf.urls import patterns, include, url
from base.models import Tab
from base.views import main_page

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Servus.views.home', name='home'),
    # url(r'^Servus/', include('Servus.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$', main_page),
    url(r'^sidebar/$', 'sidebar.views.sidebar'),
    url(r'^admin/', include(admin.site.urls)),
)

for tab_app in Tab.objects.all().values_list('app_name', flat=True):
    urlpatterns += patterns(tab_app+'.views',
        url(r'^%s/$' % tab_app, tab_app, {'current_tab':'%s' % tab_app}),
    )