# coding=utf-8
from os import walk, stat

from base.settings import MEDIA_ROOT
from base.utils import CJB
from .models import Slideshow, SlideshowChanges


class SlideshowJob(CJB):
    """
    CronJobBase класс для проверки изменений в папке media/slideshow
    и добавление/удаление альбомов с изображениями в таблицу БД slideshow.
    """

    RUN_AT_TIMES = ['04:00', ]

    @staticmethod
    def do():
        """
        Функция записи в таблицу БД base_slideshow абсолютных путей до каждого альбома,
        находящегося в папке media/slideshow.
        """

        album_paths = []

        # Преобразование в list необходимо, т.к. в противном случае мы получим объект типа:
        # <class 'django.db.models.query.ValuesListQuerySet'>
        was_excluded = list(Slideshow.objects.filter(is_shown=False).values_list('album_path', flat=True))
        obj_ssch = SlideshowChanges.objects.get_or_create(id=1)[0]
        mtime = obj_ssch.mtime
        dir_changed = False

        slideshow_folder = MEDIA_ROOT + '/slideshow'
        for root, dirs, files in walk(unicode(slideshow_folder), followlinks=True):

            # Не вносим в список album_paths пустые папки
            if len(files):
                album = root.replace(slideshow_folder, '').replace('\\', '/')
                if not album:
                    album = '/'
                album_paths.append(album)

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
