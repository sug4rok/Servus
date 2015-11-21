# coding=utf-8
from django.conf.urls import url

from .views import home, positioned, tiled

urlpatterns = [
    url(r'^$', home),
    url(r'^home/', home),
    url(r'^positioned-(?P<plan_id>[0-9]{1,4})/$', positioned),
    url(r'^tiled/$', tiled),
]
