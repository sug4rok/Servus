# coding=utf-8
from os import walk, stat
from django_cron import CronJobBase, Schedule
from Servus.Servus import SLIDESHOW_ROOT
from base.models import Slideshow, SlideshowChanges, SlideshowExclude


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

        from time import time
        t1 = time()

        album_paths = []
        try:
            mtime = SlideshowChanges.objects.get(id=1).mtime
        except SlideshowChanges.DoesNotExist:
            mtime = 0.0
        exclude_dirs = SlideshowExclude.objects.all().values_list('album_exclude', flat=True)
        dir_changed = False

        for root, dirs, files in walk(unicode(SLIDESHOW_ROOT), followlinks=True):

            # Изменение списка 'dirnames' остановит обход исключенных папок os.walk().
            for exclude_dir in exclude_dirs:
                if exclude_dir in dirs:
                    dirs.remove(exclude_dir)

            # Не вносим в список album_paths пустые папки
            amount_files = len(files)
            if amount_files:
                album_paths.append(root.replace('\\', '/'))

            # Сравниваем время модификации текущей папки со временем, хранящемся
            # в таблице БД base_slideshowchanges
            curr_mtime = stat(root).st_mtime
            print root, curr_mtime, mtime, curr_mtime > mtime
            if curr_mtime > mtime:
                mtime = curr_mtime
                dir_changed = True

        # Если хотя бы у одной папки/подпапки было изменено время последней модификации
        # или в БД были добавлены папки для ислючения их просмотра, то
        # перезаписываем таблицу БД base_slideshow
        if dir_changed or SlideshowChanges.objects.get(id=1).was_excluded:
            Slideshow.objects.all().delete()
            for album_path in album_paths:
                Slideshow.objects.create(album_path=album_path)
            obj_ssch, created = SlideshowChanges.objects.get_or_create(id=1)
            obj_ssch.mtime = mtime
            obj_ssch.was_excluded = False
            obj_ssch.save()

        print time()-t1