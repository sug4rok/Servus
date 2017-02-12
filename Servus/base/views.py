# coding=utf-8
from django.http import Http404
from django.shortcuts import render

from base.settings import SITE_NAME, THEME
from .models import Application
from events.utils import get_amount_events


def get_tab_options(active_app_name):
    """
    Функция получения названия вкладки, заголовка и краткого описания страницы для
    конкретной вкладки.

    :param active_app_name: str Имя вкладки (в базе таблица base_tab)
    :returns: dict Список параметров вкладки
    """

    tab_options = Application.objects.get(name=active_app_name)
    return {'active_title': tab_options.title,
            'active_sub_title': tab_options.sub_title}


def call_template(request, *args, **kwargs):
    """
    Универсальная функция-обработчик запросов для всех вьюшек

    :param request: django request
    :param args: словарь с дополнительными параметрами для render
    :param kwargs: на данный момент только templ_path - запрашиваемый шаблон
    """

    # Словарь для передачи параметров в render
    params = {'site_name': SITE_NAME, 'theme': THEME, 'tabs': Application.objects.filter(is_tab=1)}

    if args:
        params.update(args[0])

    if 'active_app_name' in params:
        aan = params['active_app_name']
        params.update(get_tab_options(aan))
        return render(request, '%s/tab.html' % aan, params)

    templ_path = kwargs.pop('templ_path', None)
    if templ_path is not None:
        return render(request, templ_path, params)

    raise Http404()


def amount_events(request, template, days=1):
    """
    Функция, выводящая количество и важность событий на указанную в template
    страницу за определенное количество дней.

    :param request: django request.
    :param template: str Шаблон страницы, на которой будет отображено количество
    событий.
    :param days: int Количество дней, за которые нужно вывести список событий.
    """

    request.session.save()
    current_session = request.session.session_key
    params = get_amount_events(days, session_key=current_session)

    return call_template(
        request,
        params,
        templ_path=template
    )


def navbar_events(request):
    """" Количество непросмотренных событий для отображения в меню """
    return amount_events(request, 'base/navbar_events.html', days=7)
