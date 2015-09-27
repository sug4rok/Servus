# coding=utf-8
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Application, Location


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    fields = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'password')
    readonly_fields = ('password', )

    
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_tab', 'is_widget')
    fieldsets = (
        ('', {
            'fields': ('name', 'is_widget')
        }),
        ('Настройки вкладки', {
            'fields': ('is_tab', 'tab_name', 'title', 'sub_title')
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(ApplicationAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Location, LocationAdmin)
