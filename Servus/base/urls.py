# coding=utf-8
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve
from django.conf import settings

from .views import navbar_events

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('home.urls')),
    url(r'^', include('slideshow.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'navbar_events/$', navbar_events),
]

for app in settings.CONTAINER_APPS:
    urlpatterns.append(url(r'^', include(app + '.urls')))
