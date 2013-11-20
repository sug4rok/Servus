from django.contrib import admin
from Servus.Servus import TAB_APPS
from base.models import Tab


class TabAdmin(admin.ModelAdmin):    
    list_display = ('tab_name', 'title')
    ordering = ('id',)
    fieldsets = (
        ('Основные настройки', {
                                'fields':('app_name', 'tab_name',),
                                'description':'Поля, выделенные жирным цветом, необходимо заполнить'
                                }),
        ('Дополнительно', {'fields':('title', 'sub_title'),'classes':['collapse']})
    )   

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'app_name':
            not_used_apps = []
            used_apps =  Tab.objects.all().values_list('app_name', flat=True)
            for tab_app in TAB_APPS:
                if tab_app not in used_apps:
                    not_used_apps.append((tab_app, tab_app))
            kwargs['choices'] = not_used_apps
        return super(TabAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)
   
admin.site.register(Tab, TabAdmin)