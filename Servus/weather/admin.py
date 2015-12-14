# coding=utf-8
from plugins.admin import PluginAdmin

# Определяем имя текущего плагина, настройки отображения в панели администратора
# и регистрируем его с помощью метода "register" вспомогательного класса PluginAdmin.
CONTAINER = __name__.split('.')[0]
settings = {'list_display': ('city', 'city_id', 'on_sidebar', 'is_used'),
            'ordering': ('city',)}
PluginAdmin(container, settings).register()
