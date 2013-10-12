from django.contrib import admin
from base.models import Tab
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

class Tab_WeatherAdmin(admin.ModelAdmin):
    radio_fields = {'app_name': admin.VERTICAL}
    
admin.site.register(Tab, TabAdmin)