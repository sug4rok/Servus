# coding=utf-8
from django.contrib import admin
from climate.models import TempHumidSensor


class TempHumidAdmin(admin.ModelAdmin):
    list_display = ('sensor_name', 'sensor_verb_name', 'is_used')
    ordering = ('sensor_name',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(TempHumidAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(TempHumidSensor, TempHumidAdmin)