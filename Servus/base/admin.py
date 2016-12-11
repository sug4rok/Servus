# coding=utf-8
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Application, Location


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    fields = ('username', 'first_name', 'last_name', 'email', 'is_staff',
              'is_active', 'password')
    readonly_fields = ('password',)


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_tab', 'is_widget')
    base_fieldsets = (('', {'fields': ('name', 'is_tab', 'is_widget')}),)

    def get_form(self, request, obj=None, **kwargs):
        """
        Отображение полей в зависимости от значения is_widget и is_tab, чтобы
        не отображать поля, в которых нет необходимости.
        :param request: django request
        """

        if obj is not None:
            self.fieldsets = self.base_fieldsets
            if obj.is_tab:
                self.fieldsets += (('Настройки вкладки', {'fields': ('tab_name', 'title', 'sub_title')}),)

            if obj.is_widget:
                if obj.widget_type == 'positioned':
                    self.fieldsets += (('Настройки виджета',
                                        {
                                            'fields': (
                                                'widget_type', 'plan_image', ('horiz_position', 'vert_position'))}),)
                else:
                    self.fieldsets += (('Настройки виджета', {'fields': ('widget_type',)}),)
        return super(ApplicationAdmin, self).get_form(request, obj, **kwargs)

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
