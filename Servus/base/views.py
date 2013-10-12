# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from Servus.Servus import SITE_NAME, TAB_APPS
from base.models import Tab

tabs = []
for tab in Tab.objects.all():
    if tab.app_name in  TAB_APPS:
        tabs.append(tab)
        
params = {'site_name':SITE_NAME, 'tabs':tabs}

def get_weekday(weekday):
    # Getting the name of the day of the week 
    
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
    # Getting the name of the month
    
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