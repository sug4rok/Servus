# coding=utf-8
from django.contrib import admin

from .models import Plan


class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_shown')
    ordering = ('is_shown',)


admin.site.register(Plan, PlanAdmin)
