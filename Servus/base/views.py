# -*- coding: utf-8 -*-
from os import walk, path
from random import randint
from datetime import datetime, timedelta
from django.shortcuts import render_to_response
from django.template import RequestContext
from Servus.settings import BASE_DIR, STATIC_URL
from Servus.Servus import SITE_NAME, TAB_APPS, SLIDESHOW_FILE_TYPES
from base.models import Tab, Slideshow, Events, RemoteIP

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
    
def get_remote_ip(request):
    remote_ip, ip_is_new = RemoteIP.objects.get_or_create(ip=request.META['REMOTE_ADDR'])
    last_access = False
    if not ip_is_new:
        last_access = remote_ip.last_access
        remote_ip.last_access = datetime.now()
        remote_ip.save()
    return (remote_ip.ip, last_access)
    
def get_events(ip):
    """
    События за последние 7 дней для ip-адресов не ассоциированных еще с данным событием.
    Ассоциация события с ip-адресом происходит после его закрытия в списке событий на странице home
    На входе: ip-адрес пользователя, просматривающего страницу
    На выходе: список не просмотренных или не закрытых пользователем событий за последнии 7 дней
    """
    
    try:
        events = Events.objects.filter(event_datetime__gte = datetime.now() - timedelta(days=7)).exclude(ips__ip=ip).order_by('-event_imp')
    except Events.DoesNotExist:
        events = []
        
    return events

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
        
def index(request):
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
        templ_path = 'base/index.html'
    )
      
def events(request):
    """
    Функция, выводящая количество и важность событий на главную страницу
    """
    
    pn, pv = [], []
    
    ip, last_access = get_remote_ip(request)
    
    events = get_events(ip)
    amount_events = len(events)
    if amount_events:
        pn.append('amount_events')
        pv.append(amount_events)
        pn.append('event_imp')
        pv.append(get_alert(max(events.values_list('event_imp', flat=True))))
    else:
        pn.append('amount_events')
        pv.append(0)
    return call_template(
        request,
        param_names = pn,
        param_vals = pv,
        templ_path = 'base/events.html'
    )