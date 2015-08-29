# coding=utf-8
from django.db import models
from base.settings import PLUGINS
from base.models import Location

class Plugins():
        
    def _get_plugin_model(self, plugin_package):
        model_name = plugin_package.models.MODEL        
        model_object = getattr(plugin_package.models, model_name)
        try:
            model_container = model_object.CONTAINER
        except AttributeError:
            model_container = 'system'
        try:
            model_admin = model_object.ADMIN
        except AttributeError:
            model_admin = False
            
        return {'name': model_name, 'object': model_object, 'container': model_container,
                'admin': model_admin}
        
    def _get_new_plugin_model(self, plugin_model, container):
        return type(plugin_model['name'], (plugin_model['object'], ), {
            'location': models.ForeignKey(
                Location,
                verbose_name='Расположение',
                help_text='Место расположения объекта в помещении',
            ),
            'is_used': models.BooleanField(
                verbose_name='Задействован',
                default=False
            ),
            'parent': models.OneToOneField(plugin_model['object'], parent_link=True),
            '__module__': container + '.models',
            })
    
    def get_plugin_models(self):
        plugin_models = {}
        for plugin in PLUGINS:
            plugin_package = __import__(plugin, fromlist=['models', ])
            plugin_model = self._get_plugin_model(plugin_package)
            container = plugin_model['container']
            new_plugin_model = self._get_new_plugin_model(plugin_model, container)
            new_plugin_model._meta.verbose_name = plugin_model['object']._meta.verbose_name
            new_plugin_model._meta.verbose_name_plural = plugin_model['object']._meta.verbose_name_plural
            if not plugin_models.has_key(container):
                plugin_models[container] = []
            plugin_models[container].append(new_plugin_model)
        return plugin_models

PLUGIN_MODELS = Plugins().get_plugin_models()