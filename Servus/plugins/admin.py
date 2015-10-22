# coding=utf-8
from django.contrib import admin

from plugins.models import PLUGIN_MODELS


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
        return type(plugin_model.__name__ + 'Admin', (admin.ModelAdmin, ), self._settings)
    
    @staticmethod
    def _plugin_register(plugin_model, plugin_admin):
        admin.site.register(plugin_model, plugin_admin)

    def register(self):
        for plugin_model in self._plugin_models:
            self._plugin_register(plugin_model, self._get_plugin_admin(plugin_model))
