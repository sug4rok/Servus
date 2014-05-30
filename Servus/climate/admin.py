# coding=utf-8
from django.contrib import admin
from climate.models import TempHumidSensor


class TempHumidAdmin(admin.ModelAdmin):
    list_display = ('sensor_verb_name', 'sensor_name', 'sensor_pin', 'is_used')
    ordering = ('sensor_name',)


admin.site.register(TempHumidSensor, TempHumidAdmin)