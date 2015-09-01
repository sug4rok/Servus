# coding=utf-8
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from base.settings import SITE_NAME, THEME
from .models import Application


def get_tab_options(current_tab):
    """
    Функция получения названия вкладки, заголовка и краткого описания страницы для
    конкретной вкладки.

    :param current_tab: str Имя вкладки (в базе таблица base_tab)
    :returns: dict Список параметров вкладки
    """

    tab_options = Application.objects.get(name=current_tab)
    return {'active_app_name':current_tab, 'active_title':tab_options.title,
            'active_sub_title':tab_options.sub_title}


def call_template(request, *args, **kwargs):
    """
    Универсальная функция-обработчик запросов для всех вьюшек

    :param request: django request
    :param args: словарь с дополнительными параметрами для render_to_response
    :param kwargs: на данный момент только current_tab - запрашиваемая вкладка,
                   или templ_path - запрашиваемый шаблон
    """

    # Словарь для передачи параметров с render_to_response
    params = {'site_name': SITE_NAME, 'theme': THEME, 'tabs': Application.objects.filter(is_tab=1)}

    if args:
        params.update(args[0])

    current_tab = kwargs.pop('current_tab', None)
    if current_tab is not None:
        params.update(get_tab_options(current_tab))

        # RequestContext необходим для получения текущего URL в шаблоне
        return render_to_response('%s/tab.html' % current_tab, params, context_instance=RequestContext(request))

    templ_path = kwargs.pop('templ_path', None)
    if templ_path is not None:
        return render_to_response(templ_path, params, context_instance=RequestContext(request))

    raise Http404()
