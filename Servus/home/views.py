# coding=utf-8
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.contrib.sessions.models import Session
from base.views import call_template, get_alert, get_events
from base.models import Event
from home.models import Plan
from weather.models import Weather
from weather.views import CLOUDS_RANGE, FALLS_RANGE


def position_nearest_forecast(d):
        """
        Функция получения некоторых усредненных данных прогноза погоды для активированных погодных API,
        отображаемых на Главной странице.

        :param d: день в формате datetime, для которого будем усреднять прогноз.
        :returns: словарь, с данными о температуре, скорости ветра и соответствующим облачности и
        осадкам файлам PNG.
        """

        # Создаем список объектов Weather, всех активированных прогнозных API,
        # приходящихся на переданный в функциию день с 12:00 до 16:00 включительно
        #(будем считать, что день у нас с 12 до 16 часов ;)).
        dt1 = datetime(d.year, d.month, d.day, 12)
        dt2 = datetime(d.year, d.month, d.day, 16)
        w_objs = Weather.objects.filter(wp__on_sidebar=True, datetime__range=[dt1, dt2])

        forecast = {
            'temperature': [],
            'wind_speed': [],
            'clouds_img': [],
            'falls_img': []
        }
        amount_data = len(w_objs)
        if amount_data:
            for w_obj in w_objs:
                forecast['temperature'].append(w_obj.temperature)
                forecast['wind_speed'].append(w_obj.wind_speed)
                forecast['clouds_img'].append(w_obj.clouds_img)
                forecast['falls_img'].append(w_obj.falls_img)
        else:
            return 'na'

        # Заполняем словарь forecast снова, теперь уже усредненными данными
        temperature = round(float(sum(forecast['temperature'])) / amount_data, 0)
        for f_k, f_v in forecast.iteritems():
            if f_k == 'falls_img':
                tmp_data1 = sum([float(f[1]) for f in f_v]) / amount_data
                tmp_data2 = sum([float(f[3]) for f in f_v]) / amount_data

                if tmp_data1 > 0.5:
                    if temperature > 2:
                        tmp_data1 = '1'
                    elif temperature < 0:
                        tmp_data1 = '3'
                    else:
                        tmp_data1 = '2'
                else:
                    tmp_data1 = '0'

                file_img = 't%sd%.0f' % (tmp_data1, tmp_data2)
                forecast[f_k] = [(file_img, FALLS_RANGE[file_img])]
            elif f_k == 'clouds_img':
                tmp_data1 = sum([float(f[2]) for f in f_v]) / amount_data
                file_img = 'cd%.0f' % tmp_data1
                forecast[f_k] = [(file_img, CLOUDS_RANGE[file_img[2]])]
            elif f_k == 'temperature':
                forecast[f_k] = '%d' % temperature
            else:
                forecast[f_k] = '%d' % round(float(sum(f_v)) / amount_data, 0)
        return forecast


def summary(request):

    params = {
        'forecast_today': position_nearest_forecast(datetime.today()),
        'forecast_tomorrow': position_nearest_forecast(datetime.today() + timedelta(days=1))
    }

    request.session.save()
    current_session = request.session.session_key

    # Получение списка событий для текущей сессии.
    # Если с событием еще не ассоциирован ключ данной сессии, оно добавляется в список events.
    events = get_events(current_session)
    events_data = []

    if len(events):
        for event in events:
            events_data.append((
                event.id,
                get_alert(event.event_imp),
                event.event_datetime,
                event.event_src,
                event.event_descr
            ))

    params['events'] = events_data

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

    plans = [(p.plan_name, p.plan_file) for p in Plan.objects.filter(is_shown=True)]
    params = {'house_plans': plans, }
    if len(plans):
        params['width_plans'] = 100 / len(plans)

    return call_template(
        request,
        params,
        current_tab=current_tab
    )