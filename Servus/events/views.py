# coding=utf-8
from base.views import call_template
from events.utils import get_amount_events, get_events


def events(request, current_tab):
    """
    Вывод событий последних 10 дней на вкладку События.

    :param request: django request
    :param current_tab: название текущей вкладки (передается в Servus.urls)
    """

    params = dict(events=get_events())

    return call_template(
        request,
        params,
        current_tab=current_tab
    )


def amount_events(request):
    """
    Функция, выводящая количество и важность событий на главную страницу

    :param request: django request
    """

    params = {
        'amount_events': get_amount_events(request)[0],
        'event_imp': get_amount_events(request)[1]
    }

    return call_template(
        request,
        params,
        templ_path='base/amount_events.html'
    )