# coding=utf-8
from importlib import import_module

from base.models import Application
from base.views import call_template
from .models import Plan


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
    for app in apps:
        try:
            widget = import_module(app + '.widget')
            try:
                get_widget_data = getattr(widget, 'get_widget_data')
                if app == 'events':
                    # Получение списка событий для текущей сессии.
                    params[app] = get_widget_data(current_session)
                else:
                    params[app] = get_widget_data()
                widget_pages.append(app + '/widget.html')
            except AttributeError:
                pass
        except ImportError:
            pass
    
    params['widget_pages'] = widget_pages

    return call_template(
        request,
        params,
        templ_path='home/summary.html'
    )


def home(request, current_tab):
    """
    Контроллер для вывода Главной страницы

    :param request: django request
    :param current_tab: название текущей вкладки (передается в base.urls)
    """

    plans = [(p.name, p.image) for p in Plan.objects.filter(is_shown=True)]
    params = {'house_plans': plans, }
    if len(plans):
        params['width_plans'] = 100 / len(plans)

    return call_template(
        request,
        params,
        current_tab=current_tab
    )
