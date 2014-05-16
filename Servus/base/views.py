# coding=utf-8
from os import walk, path
from random import randint
from datetime import datetime, timedelta
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from Servus.settings import MEDIA_ROOT
from Servus.Servus import SITE_NAME
from base.models import Tab, Slideshow, Slidetype, Event

# It's a dictionary of parameters for sending to render_to_response
PARAMS = {}


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

PARAMS['site_name'] = SITE_NAME
PARAMS['tabs'] = Tab.objects.filter(is_shown=1)


def get_weekday(weekday):
    """
    Функция получения названия дня недели

    :param weekday: порядковый номер дня недели
    """

    days = {
        0: u'Понедельник',
        1: u'Вторник',
        2: u'Среда',
        3: u'Четверг',
        4: u'Пятница',
        5: u'Суббота',
        6: u'Воскресенье'
    }
    return days[weekday]


def get_month(month):
    """
    Функция получения названия месяца в родительном падеже

    :param month: порядковый номер месяца
    """

    days = {
        1: u'Января',
        2: u'Февраля',
        3: u'Марта',
        4: u'Апреля',
        5: u'Мая',
        6: u'Июня',
        7: u'Июля',
        8: u'Августа',
        9: u'Сентября',
        10: u'Октября',
        11: u'Ноября',
        12: u'Декабря'
    }
    return days[month]


def get_alert(e_imp):
    """
    Функция получения степени кретичности системного события

    :param e_imp: integer степень кретичности
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
    Ассоциация события с session_key происходит после его закрытия в списке событий на странице home

    :param session_key: ключ конкретной сессии для браузера пользоватея, зарегистрированной django
    :returns: список не просмотренных или не закрытых пользователем событий за последнии 7 дней
    """

    try:
        return Event.objects.filter(event_datetime__gte=datetime.now() - timedelta(days=7)).exclude(session_keys__session_key=session_key).order_by('-event_imp')
    except Event.DoesNotExist:
        return []


def get_events_short(request):
    """
    Функция, выводящая количесво событий и их кретичность для определенной сессии.
    (См. описание к функции get_events).

    :param request: django request
    :returns: кортеж, вида (<количество сбобытий>, <кретичность>)
    """

    request.session.save()
    events_short = get_events(request.session.session_key)

    amount_events = len(events_short)
    if amount_events:
        return amount_events, get_alert(max(events_short.values_list('event_imp', flat=True)))
    else:
        return 0, 0


def get_tab_options(current_tab):
    """
    Функция получения названия вкладки, заголовка и краткого описания страницы для
    конкретной вкладки.

    :param current_tab: имя вкладки (в базе таблица base_tab)
    """

    tab_options = Tab.objects.get(app_name=current_tab)
    PARAMS['active_app_name'] = current_tab
    PARAMS['active_title'] = tab_options.title
    PARAMS['active_sub_title'] = tab_options.sub_title


def call_template(request, *args, **kwargs):
    """
    Универсальная функция-обработчик запросов для всех вьюшек

    :param request: django request
    :param args: словарь с дополнительными параметрами для render_to_response
    :param kwargs: на данный момент только current_tab - запрашиваемая вкладка,
                   или templ_path - запрашиваемый шаблон
    """

    if args:
        PARAMS.update(args[0])

    current_tab = kwargs.pop('current_tab', None)
    if current_tab is not None:
        get_tab_options(current_tab)

        # RequestContext необходим для получения текущего URL в шаблоне
        return render_to_response('%s/tab.html' % current_tab, PARAMS, context_instance=RequestContext(request))
        
    templ_path = kwargs.pop('templ_path', None)
    if templ_path is not None:
        return render_to_response(templ_path, PARAMS, context_instance=RequestContext(request))

    raise Http404()


def main_page(request):
    """
    Функция отображения начальной страницы

    :param request: django request
    """

    return call_template(
        request,
        templ_path='base/body_main.html'
    )


def slideshow(request):
    """
    Функция отображения на начальной странице произвольной фотографии

    :param request: django request
    """

    params = {}
    slide_types = Slidetype.objects.all().values_list('type', flat=True)

    if len(Slideshow.objects.all()) and slide_types:
        while True:
            try:
                # Получаем первый элемент произвольно отсортированного списка фотоальбомов,
                # исключая альбомы с пометкой is_shown = False
                rnd_album = unicode(
                    MEDIA_ROOT + Slideshow.objects.exclude(is_shown=False).order_by('?')[0].album_path
                )
                if path.exists(rnd_album):
                    for root, dirs, files in walk(rnd_album):
                        rnd_file = randint(0, len(files) - 1)
                        slide = '%s/%s' % (root.replace(MEDIA_ROOT, ''), files[rnd_file])
                        file_type = slide.split('.')[-1].lower()
                        if file_type not in slide_types:
                            raise NotImageError(file_type)
                        else:
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
    return call_template(
        request,
        params,
        templ_path='base/slideshow.html'
    )


def events(request):
    """
    Функция, выводящая количество и важность событий на главную страницу

    :param request: django request
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