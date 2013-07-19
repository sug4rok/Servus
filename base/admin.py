from django.contrib import admin
from base.models import Tab

class TabAdmin(admin.ModelAdmin):
    list_display = ('tab_name', 'title')
    ordering = ('id',)
    
admin.site.register(Tab, TabAdmin)