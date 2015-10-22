# coding=utf-8
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve

from .settings import MEDIA_ROOT
from base.models import Application

admin.autodiscover()

urlpatterns = [
    url(r'^', include('home.urls')),
    url(r'^', include('slideshow.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
]

for app in Application.objects.filter(is_tab=1).values_list('name', flat=True):
    urlpatterns.append(url(r'^', include(app + '.urls')))
