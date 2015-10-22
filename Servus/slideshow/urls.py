# coding=utf-8
from django.conf.urls import url

from .views import slideshow, slide, amount_events

urlpatterns = [
    url(r'slideshow/$', slideshow),
    url(r'slide/$', slide),
    url(r'amount_events/$', amount_events)
]
