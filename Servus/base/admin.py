# coding=utf-8
from django.contrib import admin
from Servus.Servus import TAB_APPS
from base.models import Tab, EventRule, SlideshowExclude
from weather.models import WeatherProvider


class TabAdmin(admin.ModelAdmin):
    list_display = ('tab_name', 'title')
    ordering = ('id',)
    fieldsets = (
        ('Основные настройки', {
            'fields': ('app_name', 'tab_name', 'title'),
            'description': 'Поля, выделенные жирным цветом, необходимо заполнить'
        }),
        ('Дополнительно', {'fields': ('sub_title', )})
    )

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        """
        Метод, переопределяющий типы доступных приложений. По умолчанию доступны все приложения,
        активированные (добавлненные) в настройках, но т.к. вполне достаточно иметь на каждое
        приложение по одной вкладке, то уже использованные типы приложений будут убираться из
        доступных при создании новой вкладки, или при изменении уже существующей вкладки.
        При изменении типа уже существующей вкладки, высвобожденный тип приложения становится
        снова доступным.
        """

        if db_field.name == 'app_name':
            not_used_apps = []
            used_apps =  Tab.objects.all().values_list('app_name', flat=True)
            for tab_app in TAB_APPS:
                if tab_app not in used_apps:
                    not_used_apps.append((tab_app, tab_app))
            kwargs['choices'] = not_used_apps
        return super(TabAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)


class EventRuleAdmin(admin.ModelAdmin):
    list_display = ('event_src', 'event_descr')
    ordering = ('event_src',)


class WeatherProviderAdmin(admin.ModelAdmin):
    list_display = ('weather_provider', 'weather_url', 'weather_city')
    ordering = ('weather_provider',)


class SlideshowExcludeAdmin(admin.ModelAdmin):
    list_display = ('album_exclude',)
    exclude = ('indexed',)


admin.site.register(Tab, TabAdmin)
admin.site.register(EventRule, EventRuleAdmin)
admin.site.register(SlideshowExclude)
admin.site.register(WeatherProvider, WeatherProviderAdmin)