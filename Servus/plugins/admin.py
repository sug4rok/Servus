# coding=utf-8
from django.contrib import admin

from plugins.models import PLUGIN_MODELS


class PreparePluginAdmin(admin.ModelAdmin):
    
    def get_fieldsets(self, request, obj=None):
        """
        Отображение полей в зависимости от значения is_widget чтобы не отображать
        поля, в которых нет необходимости для данного плагина.
        """
        
        # Получаем fieldsets по умолчанию и отрезаем последние 5 полей: widget_type,
        # plan_image, horiz_position и vert_position
        fieldsets = super(PreparePluginAdmin, self).get_fieldsets(request, obj)
        fieldsets[0][1]['fields'] = fieldsets[0][1]['fields'][:-4]
        
        if obj is not None:
            if obj.is_widget:
                if obj.widget_type=='positioned':
                    fieldsets += (('Настройки виджета', 
                        {'fields': ('widget_type', 'plan_image', ('horiz_position', 'vert_position'))}), )
                else:
                    fieldsets += (('Настройки виджета', {'fields': ('widget_type', )}), )
        return fieldsets


class PluginAdmin(object):
    """
    Регистрация модели плагина в административной панели.
    """

    def __init__(self, container, settings={}):
        """
        :param container: str Название приложения-контейнера, в котором будет размещен плагин.
        :param settings: dict Настройки отображения плагина в административной модели.
        """        
        self._plugin_models = PLUGIN_MODELS[container]
        self._settings = settings
        
    def _get_plugin_admin(self, plugin_model):
        return type(plugin_model.__name__ + 'Admin', (PreparePluginAdmin, ), self._settings)
    
    @staticmethod
    def _plugin_register(plugin_model, plugin_admin):
        admin.site.register(plugin_model, plugin_admin)

    def register(self):
        for plugin_model in self._plugin_models:
            self._plugin_register(plugin_model, self._get_plugin_admin(plugin_model))
