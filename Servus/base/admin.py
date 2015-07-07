# coding=utf-8
from django.contrib import admin
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group
from .models import User, Tab, Location


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')


class TabAdmin(admin.ModelAdmin):
    list_display = ('tab_name', 'title', 'is_shown')
    ordering = ('id',)
    fieldsets = (
        ('Основные настройки', {
            'fields': ('tab_name', 'title', 'is_shown'),
            'description': 'Поля, выделенные жирным цветом, необходимо заполнить'
        }),
        ('Дополнительно', {'fields': ('sub_title', )})
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(TabAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


admin.site.unregister(Group)
admin.site.unregister(DjangoUser)
admin.site.register(User, UserAdmin)
admin.site.register(Tab, TabAdmin)
admin.site.register(Location, LocationAdmin)
