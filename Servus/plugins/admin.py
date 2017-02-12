# coding=utf-8
from django.contrib import admin

from plugins.models import PLUGIN_MODELS


class PreparePluginAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(PreparePluginAdmin, self).get_readonly_fields(request, obj)

        if obj is not None:
            if hasattr(obj, 'max_value'):
                readonly_fields += ('max_value', )

            if hasattr(obj, 'min_value'):
                readonly_fields += ('min_value', )

        return readonly_fields


class PluginAdmin(object):
    """
    Регистрация модели плагина в административной панели.
    """

    def __init__(self, container, settings=None):
        """
        :param container: str Название приложения-контейнера, в котором будет размещен плагин.
        :param settings: dict Настройки отображения плагина в административной модели.
        """

        if settings is None:
            self._settings = {}
        else:
            self._settings = settings

        self._plugin_models = PLUGIN_MODELS.get(container)

    def _get_plugin_admin(self, plugin_model):
        return type(plugin_model.__name__ + 'Admin', (PreparePluginAdmin,), self._settings)

    @staticmethod
    def _plugin_register(plugin_model, plugin_admin):
        admin.site.register(plugin_model, plugin_admin)

    def register(self):
        if self._plugin_models is not None:
            for plugin_model in self._plugin_models:
                self._plugin_register(plugin_model, self._get_plugin_admin(plugin_model))
