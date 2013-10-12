# -*- coding: utf-8 -*-
from django.db import models


class MTime(models.Model):
    mtime = models.FloatField(
        default = 0.0
    )
    
    
class Slideshow(models.Model):
    album_path = models.ImageField(
        upload_to = '.'
    )

    def __unicode__(self):
        return 'Slideshow class'