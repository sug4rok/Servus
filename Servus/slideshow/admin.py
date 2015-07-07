# coding=utf-8
from django.contrib import admin
from .models import Slideshow


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


admin.site.register(Slideshow, SlideshowAdmin)
