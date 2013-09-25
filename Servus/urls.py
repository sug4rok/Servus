from django.conf.urls import patterns, include, url
from Servus import TAB_APPS

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

    url(r'^$|^home/$', 'home.views.home', {'current_tab':'home'}), 
    url(r'^sidebar/$', 'sidebar.views.sidebar'),    
    url(r'^admin/', include(admin.site.urls)),
)

for tab_app in TAB_APPS:
    urlpatterns += patterns(tab_app+'.views',
        url(r'^%s/$' % tab_app, tab_app, {'current_tab':'%s' % tab_app}),
    )