from django.db import models
from Servus.Servus import TAB_APPS

# Getting application type for a new tab
APP_NAME_CHOICES = ((tab_app, tab_app) for tab_app in TAB_APPS) 

class Tab(models.Model):     

    class Meta:
        verbose_name = 'Вкладку'
        verbose_name_plural = 'Вкладки'  
    
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
        
        
class RemoteHost(models.Model):
    ip = models.IPAddressField(
        default='127.0.0.1'
    )
    host = models.CharField(
        max_length=15
    )
    user_agent = models.TextField()
    r_hash = models.CharField(
        max_length=32,
        unique=True
    )
    last_access = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время последнего подключения'
    )
    
    def __unicode__(self):
        return self.ip

        
class Event(models.Model):
    importance = (
        (0, 'Простое сообщение'),
        (1, 'Положительное уведомление'),
        (2, 'Информация к сведению'),
        (3, 'Внимание!'),
        (4, 'Опасность!!')
    )
    event_src = models.ForeignKey(
        Tab,
        verbose_name='Источник события',
    )
    event_descr = models.CharField(
        max_length=255,
        verbose_name='Описание события',
        null=True
    )
    event_imp = models.IntegerField(
        max_length=1,
        verbose_name='Критичность',
        choices=importance,
        default=0
    )
    event_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время возникновения события'
    )
    r_hashes = models.ManyToManyField(
        RemoteHost,
        editable=False
    )

    def __unicode__(self):
        return self.event_descr   

    class Meta:
        ordering = ('event_datetime',)


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
