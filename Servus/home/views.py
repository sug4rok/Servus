# coding=utf-8
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.contrib.sessions.models import Session
from base.views import call_template, get_alert, get_events
from base.models import Event
from home.models import Plan
from weather.models import Weather
from weather.views import CLOUDS_RANGE, FALLS_RANGE


def position_nearest_forecast(day):
        """
        Функция получения некоторых усредненных данных прогноза погоды для активированных погодных API,
        отображаемых на Главной странице.

        :param day: день (число), для которого будем усреднять прогноз.
        :returns: словарь, вида с данными о температуре, скорости ветра и соответствующим облачности и
        осадкам файлам PNG.
        """

        datetimes = Weather.objects.filter(wp__on_sidebar=True).values_list('datetime', flat=True)
        value_set = {
            'temperature': Weather.objects.filter(wp__on_sidebar=True).values_list('temperature', flat=True),
            'wind_speed': Weather.objects.filter(wp__on_sidebar=True).values_list('wind_speed', flat=True),
            'clouds_img': Weather.objects.filter(wp__on_sidebar=True).exclude(clouds_img='na').values_list('clouds_img', flat=True),
            'falls_img': Weather.objects.filter(wp__on_sidebar=True).exclude(falls_img='na').values_list('falls_img', flat=True)
        }

        forecast = {
            'temperature': [],
            'wind_speed': [],
            'clouds_img': [],
            'falls_img': []
        }

        # Создаем список порядковых номеров данных, всех активированных прогнозных API,
        # приходящихся на переданный в функциию день с 12:00 до 16:00 включительно
        #(будем считать, что день у нас с 12 до 16 часов ;)).
        if len(datetimes):
            for num, d in enumerate(datetimes):
                if d.day == day and 12 <= d.hour <= 16:
                    for f_k, f_v in forecast.iteritems():
                        f_v.append(value_set[f_k][num])
        else:
            return 'na'

        # Определяем количество данных для усреднения
        amount_data = len(forecast['temperature'])

        # Заполняем словарь forecast усредненными данными (данные выбираются согласно
        # составленному ранее списку валидных порядковых номеров данных после выборки из базы
        if amount_data:
            temperature = int(round(float(sum(forecast['temperature'])) / amount_data, 0))
            for f_k, f_v in forecast.iteritems():
                if f_k == 'falls_img':
                    tmp_data1, tmp_data2 = 0.0, 0.0
                    for i in xrange(amount_data):
                        # Тип float необходим для правильного последующего округления после усреднения данных
                        tmp_data1 += float(f_v[i][1])
                        tmp_data2 += float(f_v[i][3])
                    if round(tmp_data1 / amount_data, 0):
                        if temperature > 2:
                            tmp_data1 = '1'
                        elif temperature < 0:
                            tmp_data1 = '3'
                        else:
                            tmp_data1 = '2'
                    else:
                        tmp_data1 = '0'
                    file_img = 't%sd%s' % (tmp_data1, str(int(round(tmp_data2 / amount_data, 0))))
                    forecast[f_k] = [(file_img, FALLS_RANGE[file_img])]
                elif f_k == 'clouds_img':
                    tmp_data1 = 0.0
                    for i in xrange(amount_data):
                        tmp_data1 += float(f_v[i][2])
                    file_img = 'cd%s' % str(int(round(tmp_data1 / amount_data, 0)))
                    forecast[f_k] = [(file_img, CLOUDS_RANGE[file_img[2]])]
                elif f_k == 'temperature':
                    forecast[f_k] = str(temperature)
                else:
                    forecast[f_k] = str(int(round(float(sum(f_v)) / amount_data, 0)))
        else:
            return 'na'
        return forecast


def summary(request):

    params = {
        'forecast_today': position_nearest_forecast(datetime.now().day),
        'forecast_tomorrow': position_nearest_forecast((datetime.now() + timedelta(days=1)).day)
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