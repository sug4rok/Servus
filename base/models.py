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