# coding=utf-8
from os import walk, stat
from django_cron import CronJobBase, Schedule
from Servus.Servus import SLIDESHOW_ROOT
from base.models import Slideshow, SlideshowChanges


class SlideshowJob(CronJobBase):
    #RUN_EVERY_MINS = 60
    RETRY_AFTER_FAILURE_MINS = 5
    RUN_AT_TIMES = ['04:00']
    
    schedule = Schedule(
        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS,
        run_at_times=RUN_AT_TIMES
        #run_every_mins=RUN_EVERY_MINS
    )
    code = 'SlideshowJob'    # a unique code

    @staticmethod
    def do():
        """
        Функция записи в таблицу БД base_slideshow абсолютных путей до каждого альбома,
        находящегося в папке SLIDESHOW_ROOT (см. настройки Servus/Servus.py).
        """

        album_paths = []

        # Преобразование в list необходимо, т.к. в противном случае мы получим объект типа:
        # <class 'django.db.models.query.ValuesListQuerySet'>
        was_excluded = list(Slideshow.objects.filter(is_shown=False).values_list('album_path', flat=True))
        obj_ssch, created = SlideshowChanges.objects.get_or_create(id=1)
        mtime = obj_ssch.mtime
        dir_changed = False

        for root, dirs, files in walk(unicode(SLIDESHOW_ROOT), followlinks=True):

            # Не вносим в список album_paths пустые папки
            amount_files = len(files)
            if amount_files:
                album_paths.append(root.replace('\\', '/'))

            # Сравниваем время модификации текущей папки со временем, хранящемся
            # в таблице БД base_slideshowchanges
            curr_mtime = stat(root).st_mtime
            if curr_mtime > mtime:
                mtime = curr_mtime
                dir_changed = True

        # Если хотя бы у одной папки/подпапки было изменено время последней модификации,
        # то перезаписываем таблицу БД base_slideshow
        if dir_changed:
            Slideshow.objects.all().delete()
            for album_path in album_paths:
                Slideshow.objects.create(album_path=album_path, is_shown=(album_path not in was_excluded))
            obj_ssch.mtime = mtime
            obj_ssch.save()