# coding=utf-8
from django.conf.urls import url

from .views import events, set_viewed_events

urlpatterns = [
    url(r'set_viewed_events/$', set_viewed_events),
    url(r'events/$', events),
]
