from django.contrib import admin
from base.models import Tab, Event
from weather.models import Weather

    
class WeatherInline(admin.TabularInline):
    model = Weather
    extra = 1
    max_num = 1
    
    
class TabAdmin(admin.ModelAdmin):    
    list_display = ('tab_name', 'title')
    ordering = ('id',)
    fieldsets = (
        ('Основные настройки', {
                                'fields':('app_name', 'tab_name',),
                                'description':'Поля, выделенные жирным цветом, необходимо заполнить'
                                }),
        ('Дополнительно', {'fields':('title', 'sub_title')})
    )
    inlines = [
        #WeatherInline
    ]    

   
admin.site.register(Tab, TabAdmin)
#admin.site.register(Event)
