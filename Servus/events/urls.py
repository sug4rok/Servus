# coding=utf-8
from django.conf.urls import url

from .views import events

urlpatterns = [
    url(r'events/$', events),
]
