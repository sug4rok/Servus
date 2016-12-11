# coding=utf-8
from django.conf.urls import url

from .views import slideshow, slide, slideshow_events

urlpatterns = [
    url(r'slideshow/$', slideshow),
    url(r'slide/$', slide),
    url(r'slideshow_events/$', slideshow_events),
]
