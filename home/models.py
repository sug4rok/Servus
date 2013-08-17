# -*- coding: utf-8 -*-
from django.db import models
from base.models import Tab

class Tab_Home(models.Model):
    app_name = models.ForeignKey(Tab)
    
    def __unicode__(self):
        return self.home_title