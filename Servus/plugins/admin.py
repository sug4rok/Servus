# coding=utf-8
from django.contrib import admin
from .models import Plugin


class PluginAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_widget', 'is_used')
    fieldsets = (
        ('', {
            'fields': ('name', 'is_used')
        }),
        ('Настройки виджета', {
            'fields': ('is_widget', 'location')
        }),
    )


    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(PluginAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

        
admin.site.register(Plugin, PluginAdmin)