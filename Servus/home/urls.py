# coding=utf-8
from django.conf.urls import url

from .views import home, summary

urlpatterns = [
    url(r'^$', 'home.views.home'),
    url(r'^home/', 'home.views.home'),
    url(r'^summary/$', summary),
]
