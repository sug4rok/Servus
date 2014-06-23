# coding=utf-8
from django.contrib import admin
from django.contrib.auth.models import User, Group
from base.models import UserProfile, Tab, Slideshow


class UserProfileAdmin(admin.ModelAdmin):
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


class EventRuleAdmin(admin.ModelAdmin):
    list_display = ('event_src', 'event_descr')
    ordering = ('event_src',)


class SlideshowAdmin(admin.ModelAdmin):
    list_display = ('album_path', 'is_shown')
    list_filter = ('is_shown',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(SlideshowAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Tab, TabAdmin)
admin.site.register(Slideshow, SlideshowAdmin)