# coding=utf-8
from django.conf.urls import url

from .views import climate

urlpatterns = [
    url(r'climate/$', climate),
]
