# coding=utf-8
from importlib import import_module
import logging

from base.models import Application
from base.views import call_template
from .models import Plan
from plugins.utils import get_widget_plugin_names

logger = logging.getLogger(__name__)


def summary(request):
    """
    Контроллер для ajax-запроса обновления информации на Главной странице.
    Получаем список приложений, для которых создан виджет (т.е. поле is_widget=True).
    :param request: django request
    """

    request.session.save()
    current_session = request.session.session_key
    
    params = {}
    widget_pages = []

    # Получаем данные с виджетов приложений
    apps = Application.objects.filter(is_widget=1).values_list('name', flat=True)
    plugins = get_widget_plugin_names()
    widget_apps = list(apps) + plugins

    for app in widget_apps:
        try:
            widget = import_module(app + '.widget')
            if 'plugins' in app:
                app = app.split('.')[1]
 
            try:
                widget_data = {}
                get_widget_data = getattr(widget, 'get_widget_data')
                
                if app == 'events':
                    # Получение списка событий для текущей сессии.
                    widget_data = get_widget_data(current_session)
                else:
                    widget_data = get_widget_data()
                
                # Если есть данные для виджета, добавляем его html-страницу к списку страниц виджетов
                if widget_data:
                    params[app] = widget_data['data']
                    widget_pages.append((widget_data['widget_type'], app + '/widget.html'))

            except AttributeError:
                logger.error(app + ': widget module hasn\'t get_widget_data function.')
        except ImportError:
            logger.error(app + ': widget module ImportError.')
    
    params['widget_pages'] = widget_pages

    return call_template(
        request,
        params,
        templ_path='home/summary.html'
    )


def home(request):
    """
    Контроллер для вывода Главной страницы

    :param request: django request
    """

    plans = [(p.name, p.image) for p in Plan.objects.filter(is_shown=True)]
    params = {'active_app_name': 'home', 'house_plans': plans, }
    
    if len(plans):
        params['width_plans'] = 100 / len(plans)

    return call_template(request, params)
