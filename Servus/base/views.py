# coding=utf-8
from os import walk, path
from random import randint
from datetime import datetime, timedelta
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from Servus.Servus import SITE_NAME, TAB_APPS, SLIDESHOW_FILE_TYPES
from base.models import Tab, Slideshow, Event


class NotImageError(Exception):

    def __init__(self, file_type):
        self.file_type = file_type

    def __str__(self):
        return repr('NotImageError: type of file is [%s]' % self.file_type)


class PathNotFound(Exception):

    def __init__(self, broken_path):
        self.broken_path = broken_path

    def __str__(self):
        return repr('PathNotFound: [%s] is not in slideshow directory.' % self.broken_path)

tabs = []
for tab in Tab.objects.all():
    if tab.app_name in TAB_APPS:
        tabs.append(tab)

params = {'site_name': SITE_NAME, 'tabs': tabs}


def get_weekday(weekday):
    """
    Getting the name of the day of the week 
    """

    days = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота',
        6: 'Воскресенье'
    }
    return days[weekday]


def get_month(month):
    """
    Getting the name of the month
    """

    days = {
        1: 'Января',
        2: 'Февраля',
        3: 'Марта',
        4: 'Апреля',
        5: 'Мая',
        6: 'Июня',
        7: 'Июля',
        8: 'Августа',
        9: 'Сентября',
        10: 'Октября',
        11: 'Ноября',
        12: 'Декабря'
    }
    return days[month]


def get_alert(e_imp):
    """
    The function to determine the status of the event by its code
    """

    e_status = {
        0: 'default',
        1: 'success',
        2: 'info',
        3: 'warning',
        4: 'danger'
    }
    return e_status[e_imp]


def get_events(session_key):
    """
    События за последние 7 дней для сессий, не ассоциированных еще с данным событием.
    Ассоциация события с ip-адресом происходит после его закрытия в списке событий на странице home
    На входе: ip-адрес пользователя, просматривающего страницу
    На выходе: список не просмотренных или не закрытых пользователем событий за последнии 7 дней
    """

    try:
        return Event.objects.filter(event_datetime__gte=datetime.now() - timedelta(days=7)).exclude(session_keys__session_key=session_key).order_by('-event_imp')
    except Event.DoesNotExist:
        return []


def get_events_short(request):
    """
    Функция, выводящая количесво событий и их кретичность для определенной сессии.
    (См. описание к функции get_events).
    На входе: request
    На выходе: кортеж, вида (<количество сбобытий>, <кретичность>)
    """

    events_short = get_events(request.session.session_key)

    amount_events = len(events_short)
    if amount_events:
        return amount_events, get_alert(max(events_short.values_list('event_imp', flat=True)))
    else:
        return 0, 0


def get_tab_options(current_tab):
    tab_options = Tab.objects.get(app_name=current_tab)
    params['active_app_name'] = current_tab
    params['active_title'] = tab_options.title
    params['active_sub_title'] = tab_options.sub_title


def call_template(request, *args, **kwargs):
    if args:
        params.update(args[0])

    current_tab = kwargs.pop('current_tab', None)
    if current_tab is not None:
        get_tab_options(current_tab)

        # RequestContext необходим для получения текущего URL в шаблоне
        return render_to_response('%s/tab.html' % current_tab, params, context_instance=RequestContext(request))
        
    templ_path = kwargs.pop('templ_path', None)
    if templ_path is not None:
        return render_to_response(templ_path, params, context_instance=RequestContext(request))

    raise Http404()


def main_page(request):
    """
    Функция отображения начальной страницы
    """

    return call_template(
        request,
        templ_path='base/body_main.html'
    )


def slideshow(request):
    """
    Функция отображения на начальной странице произвольной фотографии
    """

    params = {'album': '', 'slide': ''}

    if Slideshow.objects.count():
        while True:
            try:
                # Получаем первый элемент произвольно отсортированного списка фотоальбомов
                rnd_album = unicode(Slideshow.objects.order_by('?')[0].album_path)
                if path.exists(rnd_album):
                    for root, dirs, files in walk(rnd_album):
                        rnd_file = randint(0, len(files) - 1)
                        slide = '%s/%s' % (root, files[rnd_file])
                        file_type = slide.split('.')[-1].lower()
                        if file_type not in SLIDESHOW_FILE_TYPES:
                            raise NotImageError(file_type)
                        params['album'] = rnd_album.split('/')[-1].replace('_', ' ')
                        params['slide'] = slide
                        break
                else:
                    raise PathNotFound(rnd_album)
            except NotImageError as e:
                print e
                continue
            except PathNotFound as e:
                print e
                continue
            else:
                break
    else:
        params['album'] = 'Нет доступных альбомов, либо они еще не проиндексированы'

    return call_template(
        request,
        params,
        templ_path='base/slideshow.html'
    )


def events(request):
    """
    Функция, выводящая количество и важность событий на главную страницу
    """

    params = {
        'amount_events': get_events_short(request)[0],
        'event_imp': get_events_short(request)[1]
    }

    return call_template(
        request,
        params,
        templ_path='base/events.html'
    )