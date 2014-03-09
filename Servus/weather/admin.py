# coding=utf-8
from django.contrib import admin
from weather.models import WeatherProvider


class WeatherProviderAdmin(admin.ModelAdmin):
    list_display = ('weather_provider', 'weather_url', 'weather_city')
    ordering = ('weather_provider',)


admin.site.register(WeatherProvider, WeatherProviderAdmin)

