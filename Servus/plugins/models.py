# coding=utf-8
from django.db import models
from base.settings import PLUGINS
from base.models import Location


class Plugins():
    """
    Класс для автоматического добавления классов-моделей плагинов (список
    плагинов берется из настроек base.settings) в модели указанных в плагинах
    приложения-контейнеры.
    """
        
    def _get_plugin_model(self, plugin_package):
        """
        Метод возвращает модель плагина, указанный в переменной 
        <some_plugin>.models.MODEL
        
        :param plugin_package: module  Пакет плагина
        :returns: <class 'django.db.models.base.ModelBase'> Модель плагина
        """
        
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
        """
        Метод возвращает новую модель плагина, основанную на ранее подгруженной.
        В новую модель добавлены обязательные для всех плагинов атрибуты.
        
        :param plugin_model: <class 'django.db.models.base.ModelBase'> Модель плагина
        :param container: str Название приложения-контейнера для плагина
        :returns: <class 'django.db.models.base.ModelBase'> Новая модель плагина
        """
        
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
            '__module__': container + '.models',  # Меняем имя модуля, содержащего новый класс
            })
    
    def get_plugin_models(self):
        """
        Метод возвращает словарь, в котором ключи - названия контейнеров плагинов,
        а значения ключей - списки моделей плагинов, относящихся к данным контейнерам.
        
        :returns: dict Словарь, вида {'container1': [model_object1, model_object2,..],..}
        """
        
        plugin_models = {}
        
        for plugin in PLUGINS:
            plugin_package = __import__(plugin, fromlist=['models', ])
            plugin_model = self._get_plugin_model(plugin_package)
            container = plugin_model['container']
            new_plugin_model = self._get_new_plugin_model(plugin_model, container)
            # Переопределяем атрибуты класса Meta у новых моделей родительскими
            new_plugin_model._meta.verbose_name = plugin_model['object']._meta.verbose_name
            new_plugin_model._meta.verbose_name_plural = plugin_model['object']._meta.verbose_name_plural
            
            if not plugin_models.has_key(container):
                plugin_models[container] = []
            plugin_models[container].append(new_plugin_model)
            
        return plugin_models

PLUGIN_MODELS = Plugins().get_plugin_models()
