# coding=utf-8
from django.contrib import admin
from plugins.models import PLUGIN_MODELS

for plugin_model in PLUGIN_MODELS[__name__.split('.')[0]]:
    admin.site.register(plugin_model)
