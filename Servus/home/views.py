# coding=utf-8
from importlib import import_module
import logging

from base.models import Application
from base.views import call_template
from .models import Plan
from plugins.utils import get_widget_plugin_names

logger = logging.getLogger(__name__)


def widgets_data(request, widget_apps, widget_type='tiled', plan_id=0):
    params = {}
    widget_pages = []

    for app in widget_apps:
        try:
            widget = import_module(app + '.widget')
            if 'plugins' in app:
                app = app.split('.')[1]

            try:
                widget_data = {}
                get_widget_data = getattr(widget, 'get_widget_data')
                try:
                    widget_data = get_widget_data(plan_id) if plan_id else get_widget_data()
                except:
                    pass

                # Если есть данные для виджета, добавляем его html-страницу к списку страниц виджетов
                if widget_data:
                    params[app] = widget_data
                    widget_pages.append(app + '/widget.html')

            except AttributeError:
                logger.error(app + ': widget module hasn\'t get_widget_data function.')
        except ImportError:
            logger.error(app + ': widget module ImportError.')

    params[widget_type] = widget_pages

    return params


def positioned(request, plan_id=1):
    """
    Контроллер для ajax-запроса обновления информации на Главной странице.
    Получаем список приложений, для которых создан позиционный виджет (т.е. поле is_widget=True).
    :param request: django request
    """

    # Получаем данные с виджетов приложений
    widget_apps = get_widget_plugin_names('positioned')

    params = widgets_data(request, widget_apps, widget_type='positioned', plan_id=int(plan_id))

    return call_template(
        request,
        params,
        templ_path='home/positioned.html'
    )


def tiled(request):
    """
    Контроллер для ajax-запроса обновления информации на Главной странице.
    Получаем список приложений, для которых создан плиточный виджет (т.е. поле is_widget=True).
    :param request: django request
    """

    # Получаем данные с виджетов приложений
    apps = Application.objects.filter(is_widget=1).values_list('name', flat=True)
    plugins = get_widget_plugin_names('tiled')
    widget_apps = list(apps) + plugins

    params = widgets_data(request, widget_apps, widget_type='tiled')

    return call_template(
        request,
        params,
        templ_path='home/tiled.html'
    )


def home(request):
    """
    Контроллер для вывода Главной страницы

    :param request: django request
    """

    plans = [(p.id, p.image, p.description) for p in Plan.objects.filter(is_shown=True)]
    params = {'active_app_name': 'home', 'house_plans': plans, }

    if len(plans):
        params['width_plans'] = 100 / len(plans)

    return call_template(request, params)
