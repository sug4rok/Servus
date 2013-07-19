from django.db import models

class Tab(models.Model):
    app_name = models.CharField(max_length=20, verbose_name='Имя приложения')
    tab_name = models.CharField(max_length=20, verbose_name='Вкладка')
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    sub_title = models.CharField(max_length=50, verbose_name='Краткое описание')

    def __unicode__(self):
	    return self.tab_name