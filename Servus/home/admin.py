# coding=utf-8
from django.contrib import admin
from home.models import Plan


class PlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'is_shown')
    ordering = ('is_shown',)


admin.site.register(Plan, PlanAdmin)