﻿# -*- coding: utf-8 -*-
from django.db import models
from base.models import Tab

class Tab_Climate(models.Model):
    app_name = models.ForeignKey(Tab)
    
    def __unicode__(self):
        return self.climate_title