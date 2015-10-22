# coding=utf-8
from plugins.admin import PluginAdmin

# Определяем имя текущего плагина, настройки отображения в панели администратора
# и регистрируем его с помощью метода "register" вспомогательного класса PluginAdmin.
container = __name__.split('.')[0]
settings = {'list_display': ('name', 'location', 'is_used'),
            'ordering': ('name',)}
PluginAdmin(container, settings).register()
