# coding=utf-8
from django.contrib import admin

from plugins.models import PLUGIN_MODELS

for plugin_model in PLUGIN_MODELS[__name__.split('.')[0]]:
    PluginAdmin = type(plugin_model.__name__ + 'Admin', (admin.ModelAdmin, ), {
        'list_display': ('city', 'url', 'on_sidebar', 'is_used'),
        'ordering': ('city',),
        })
    admin.site.register(plugin_model, PluginAdmin)

