# coding=utf-8
from django.contrib import admin

from plugins.admin import PluginAdmin
from .models import Plan


# ���������� ��� �������� �������, ��������� ����������� � ������ ��������������
# � ������������ ��� � ������� ������ "register" ���������������� ������ PluginAdmin.
CONTAINER = __name__.split('.')[0]
SETTINGS = {'list_display': ('name', 'location', 'is_used'),
            'ordering': ('name',)}
PluginAdmin(CONTAINER, SETTINGS).register()


class PlanAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_shown')
    ordering = ('is_shown',)


admin.site.register(Plan, PlanAdmin)
