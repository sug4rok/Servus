# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from Servus.Servus import SITE_NAME
from Servus.settings import STATIC_URL
from base.models import Tab

params = {'site_name':SITE_NAME,'static_url':STATIC_URL, 'tabs':Tab.objects.all()}

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
    current_tab = kwargs.pop('current_tab', None)
    get_tab_options(current_tab)
    param_vals = kwargs.pop('param_vals', None)
    for num, param in enumerate(kwargs.pop('param_names', None)):
        params[param] = param_vals[num]
    return render_to_response('%s/tab.html' % current_tab, params)