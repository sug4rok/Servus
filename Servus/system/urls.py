# coding=utf-8
from django.conf.urls import url

from home.views import home

urlpatterns = [
    url(r'^$', home),
]
