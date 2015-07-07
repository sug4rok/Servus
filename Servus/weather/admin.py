# coding=utf-8
from django.contrib import admin
from .models import WeatherProvider


class WeatherProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'is_used')
    ordering = ('name',)


admin.site.register(WeatherProvider, WeatherProviderAdmin)
