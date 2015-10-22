# coding=utf-8
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from base.settings import SITE_NAME, THEME
from .models import Application


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
    :param args: словарь с дополнительными параметрами для render_to_response
    :param kwargs: на данный момент только templ_path - запрашиваемый шаблон
    """

    # Словарь для передачи параметров с render_to_response
    params = {'site_name': SITE_NAME, 'theme': THEME, 'tabs': Application.objects.filter(is_tab=1)}

    if args:
        params.update(args[0])

    if 'active_app_name' in params:
        aan = params['active_app_name']
        params.update(get_tab_options(aan))

        # RequestContext необходим для получения текущего URL в шаблоне
        return render_to_response('%s/tab.html' % aan, params, context_instance=RequestContext(request))

    templ_path = kwargs.pop('templ_path', None)
    if templ_path is not None:
        return render_to_response(templ_path, params, context_instance=RequestContext(request))

    raise Http404()
