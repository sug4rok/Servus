# -*- coding: utf-8 -*-
from os import walk, path
from random import randint
from hashlib import md5
from datetime import datetime, timedelta
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from Servus.settings import BASE_DIR, STATIC_URL
from Servus.Servus import SITE_NAME, TAB_APPS, SLIDESHOW_FILE_TYPES
from base.models import Tab, Slideshow, Event, RemoteHost

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
    if tab.app_name in  TAB_APPS:
        tabs.append(tab)
        
params = {'site_name':SITE_NAME, 'tabs':tabs}

def get_weekday(weekday):
    """
    Getting the name of the day of the week 
    """
    
    days = {
        0:'Понедельник',
        1:'Вторник',
        2:'Среда',
        3:'Четверг',
        4:'Пятница',
        5:'Суббота',
        6:'Воскресенье'
    }
    return days[weekday]
    
def get_month(month):
    """
    Getting the name of the month
    """
    
    days = {
        1:'Января',
        2:'Февраля',
        3:'Марта',
        4:'Апреля',
        5:'Мая',
        6:'Июня',
        7:'Июля',
        8:'Августа',
        9:'Сентября',
        10:'Октября',
        11:'Ноября',
        12:'Декабря'
    }
    return days[month]
    
def get_alert(e_imp):
    """
    The function to determine the status of the event by its code
    """
    
    e_status = {
        0:'default',
        1:'success',
        2:'info',
        3:'warning',
        4:'danger'
    }
    return e_status[e_imp]
    
def get_remote_hash(request):
    """
    Функция получения MD5-хеша по полученным META-данным о удаленном хосте 
    и запись данных META и хеша в базу данных.
    На входе: request
    На выходе: расчитанный хеш, время последнего посещения.
    """
    
    r_ip, r_host, user_agent = request.META['REMOTE_ADDR'], request.META['REMOTE_HOST'], request.META['HTTP_USER_AGENT']
    r_hash = md5(r_ip + r_host + user_agent).hexdigest()
    r_hash_obj, hash_is_new = RemoteHost.objects.get_or_create(r_hash=r_hash)  

    if hash_is_new:
        last_access = False
        r_hash_obj.ip, r_hash_obj.host, r_hash_obj.user_agent = r_ip, r_host, user_agent
        
    else:
        last_access = r_hash_obj.last_access
        r_hash_obj.last_access = datetime.now()
    
    r_hash_obj.save()
    return r_hash, last_access
    
def get_events(r_hash):
    """
    События за последние 7 дней для ip-адресов не ассоциированных еще с данным событием.
    Ассоциация события с ip-адресом происходит после его закрытия в списке событий на странице home
    На входе: ip-адрес пользователя, просматривающего страницу
    На выходе: список не просмотренных или не закрытых пользователем событий за последнии 7 дней
    """
    
    try:
        return Event.objects.filter(event_datetime__gte = datetime.now() - timedelta(days=7)).exclude(r_hashes__r_hash=r_hash).order_by('-event_imp')
    except Events.DoesNotExist:
        return []
    
def get_events_short(request):
    """
    Функция, выводящая количесво событий и их кретичность для определенного хеша.
    (См. описание к функции get_events).
    На входе: request
    На выходе: кортеж, вида (<количество сбобытий>, <кретичность>)
    """
    
    r_hash, last_access = get_remote_hash(request)    
    events_short = get_events(r_hash)
    
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
    
def call_template(request, **kwargs):
    param_vals = kwargs.pop('param_vals', None)
    for num, param in enumerate(kwargs.pop('param_names', None)):
        params[param] = param_vals[num]
        
    current_tab = kwargs.pop('current_tab', None)
    if current_tab:
        get_tab_options(current_tab)
        
        # RequestContext необходим для получения текущего URL в шаблоне
        return render_to_response('%s/tab.html' % current_tab, params, context_instance=RequestContext(request))
        
    templ_path = kwargs.pop('templ_path', None)
    if templ_path:
        return render_to_response(templ_path, params, context_instance=RequestContext(request))
        
    raise Http404()
        
def main_page(request):
    """
    Функция отображения начальной страницы с выводом произвольной фотографии
    """
    
    pn, pv = [], []
    
    pn.append('album')
    pn.append('slide')
    
    path_to_imgs = '%s%simg/slideshow' % (BASE_DIR.replace('\\', '/'), STATIC_URL)    
        
    if len(Slideshow.objects.all()):
        latest_id = Slideshow.objects.latest('id').id
        while True:
            try:
                rnd_id = randint(1, latest_id)
                rnd_album = unicode(Slideshow.objects.get(id=rnd_id).album_path)
                if path.exists(rnd_album):
                    for root, dirs, files in walk(rnd_album):
                        rnd_file = randint(0, len(files) - 1)  
                        slide = '%s/%s' % (rnd_album.replace(path_to_imgs, ''), files[rnd_file])
                        file_type = slide.split('.')[-1].lower()
                        if file_type not in SLIDESHOW_FILE_TYPES:
                            raise NotImageError(file_type)
                        pv.append(rnd_album.split('/')[-1])
                        pv.append(slide)
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
        pv.append('Нет доступных альбомов, либо они еще не проиндексированы')
        pv.append('')
        
    return call_template(
        request,
        param_names = pn,
        param_vals = pv,
        templ_path = 'base/body_main.html'
    )
      
def events(request):
    """
    Функция, выводящая количество и важность событий на главную страницу
    """
    
    pn, pv = [], []
    
    pn.append('amount_events')
    pv.append(get_events_short(request)[0])
    pn.append('event_imp')
    pv.append(get_events_short(request)[1])
        
    return call_template(
        request,
        param_names = pn,
        param_vals = pv,
        templ_path = 'base/events.html'
    )
