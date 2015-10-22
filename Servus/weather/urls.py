# coding=utf-8
from django.conf.urls import url

from .views import weather

urlpatterns = [
    url(r'weather/$', weather),
]
