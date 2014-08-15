# coding=utf-8
from django.http import HttpResponseRedirect
from django.contrib.sessions.models import Session
from base.views import call_template
from events.models import Event
from events.views import get_events
from .models import Plan
from .utils import nearest_forecast, get_temp_humid


def summary(request):
    """
    Контроллер для ajax-запроса обновления информации на Главной странице.

    :param request: django request
    """

    # Отображение краткой сводки прогноза погоды на сегодня и завтра и
    # текущего значения температуры и влажности в помещениях
    params = {
        'forecasts': (nearest_forecast('сегодня'), nearest_forecast('завтра')),
        'sensors': get_temp_humid()
    }

    # Получение списка событий для текущей сессии.
    # Если с событием еще не ассоциирован ключ данной сессии, оно добавляется в список events.
    request.session.save()
    current_session = request.session.session_key

    params['events'] = get_events(current_session)

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
    :param current_tab: название текущей вкладки (передается в Servus.urls)
    """

    plans = [(p.plan_name, p.plan_file) for p in Plan.objects.filter(is_shown=True)]
    params = {'house_plans': plans, }
    if len(plans):
        params['width_plans'] = 100 / len(plans)

    return call_template(
        request,
        params,
        current_tab=current_tab
    )