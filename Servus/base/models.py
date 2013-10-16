from django.db import models
from Servus.Servus import TAB_APPS

# Getting application type for a new tab
APP_NAME_CHOICES = ((tab_app, tab_app) for tab_app in TAB_APPS) 

class Tab(models.Model):                 
    app_name = models.CharField(
        max_length=20,
        choices=APP_NAME_CHOICES,
        verbose_name='Тип приложения',
        help_text='Тип ассоциированного с данной вкладкой приложения Django'
    )
    tab_name = models.CharField(
        max_length=20,
        verbose_name='Вкладка'
    )
    title = models.CharField(
     max_length=50,
     verbose_name='Заголовок'
    )
    sub_title = models.CharField(
         max_length=100,
         verbose_name='Краткое описание',
         blank=True, 
         null=True
    )

    def __unicode__(self):
        return self.tab_name

        
class Events(models.Model):
    event_src = models.CharField(
        max_length=15,
        verbose_name='Источник события'
    )
    event_descr = models.CharField(
        max_length=255,
        verbose_name='Описание события',
        null=True
    )
    event_imp = models.IntegerField(
        max_length=1,
        verbose_name='Критичность',
        default=0,
    )
    event_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время возникновения события'
    )
    event_viewed = models.BooleanField(
        default=False,
    )

    
class Errors(models.Model):
    error_src = models.CharField(
        max_length=15,
        verbose_name='Источник ошибки'
    )
    error_descr = models.CharField(
        max_length=255,
        verbose_name='Описание ошибки',
        null=True
    )
    error_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время возникновения ошибки'
    )
    error_viewed = models.BooleanField(
        default=False
    )
    
    
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