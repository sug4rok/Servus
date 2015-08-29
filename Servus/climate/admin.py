# coding=utf-8
from django.contrib import admin
from plugins.models import PLUGIN_MODELS
from .models import TempHumidSensor


class TempHumidSensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'arduino_pin', 'location', 'location_type', 'is_used')
    ordering = ('name',)


admin.site.register(TempHumidSensor, TempHumidSensorAdmin)
for plugin_model in PLUGIN_MODELS[__name__.split('.')[0]]:
    admin.site.register(plugin_model)
