# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.shortcuts import render_to_response
from Servus.Servus import SITE_NAME
from base.models import Tab

site_name = SITE_NAME
static_url = settings.STATIC_URL

def get_tab_options(active_app_name):
    tab_options = Tab.objects.get(app_name=active_app_name)
    params['active_app_name'] = active_app_name
    params['active_title'] = tab_options.title
    params['active_sub_title'] = tab_options.sub_title    

params = {'site_name':site_name,'static_url':static_url, 'tabs':Tab.objects.all()}