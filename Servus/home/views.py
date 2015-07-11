# coding=utf-8
from importlib import import_module
from django.http import HttpResponseRedirect
from django.contrib.sessions.models import Session
from base.views import call_template
from base.settings import EXTENDED_APPS
from events.models import Event
from events.views import get_events
from .models import Plan


def summary(request):
    """
    Контроллер для ajax-запроса обновления информации на Главной странице.
    Получаем список всех доступных плагинов и отображаем виджет каждого плагина,
    если он есть.
    :param request: django request
    """

    params = {}
    widget_pages = []

    # Получаем данные с виджетов плагинов, если они виджеты есть (функция widget в файле plugin.views
    for app in EXTENDED_APPS:
        try:
            views = import_module(app + '.views')
            try:
                widget = getattr(views, 'widget')
                params[app] = widget()
                widget_pages.append(app + '/widget.html')
            except AttributeError:
                pass
        except ImportError:
            pass
    params['widget_pages'] = widget_pages

    # Получение списка событий для текущей сессии.
    # Если с событием еще не ассоциирован ключ данной сессии, оно добавляется в список events.
    request.session.save()
    current_session = request.session.session_key

    # params['events'] = get_events(current_session)

    # Обработка нажатия кнопки "x" на определнном событии.
    # (Ассоциируем с данным событием определенный ключ сессии).
    if request.method == 'POST':
        event_id = request.POST.get('event_id', '')
        if event_id:
            Event.objects.get(id=event_id).session_keys.add(Session.objects.get(pk=current_session))
            return HttpResponseRedirect('/home/')

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
