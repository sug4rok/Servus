# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.shortcuts import render_to_response
from Servus.Servus import SITE_NAME
from base.models import Tab

site_name = SITE_NAME
static_url = settings.STATIC_URL

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

def get_tab_options(active_app_name):
    tab_options = Tab.objects.get(app_name=active_app_name)
    params['active_app_name'] = active_app_name
    params['active_title'] = tab_options.title
    params['active_sub_title'] = tab_options.sub_title    

params = {'site_name':site_name,'static_url':static_url, 'tabs':Tab.objects.all()}