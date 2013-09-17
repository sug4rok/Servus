from django.contrib import admin
from base.models import Tab
from home.models import Tab_Home
from climate.models import Tab_Climate
from weather.models import Weather


class Tab_HomeInline(admin.StackedInline):
    model = Tab_Home
    extra = 1
    max_num = 1
    
class Tab_ClimateInline(admin.StackedInline):
    model = Tab_Climate
    extra = 1
    max_num = 1
    
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
        #Tab_HomeInline,
        #Tab_ClimateInline,
        #WeatherInline
    ]    

class Tab_WeatherAdmin(admin.ModelAdmin):
    radio_fields = {'app_name': admin.VERTICAL}
    
admin.site.register(Tab, TabAdmin)