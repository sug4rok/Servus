# coding=utf-8
from django.contrib import admin
from .models import TempHumidSensor


class TempHumidSensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'arduino_pin', 'location', 'location_type', 'is_used')
    ordering = ('name',)


admin.site.register(TempHumidSensor, TempHumidSensorAdmin)
