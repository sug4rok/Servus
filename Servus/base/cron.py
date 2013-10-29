from os import walk, stat
from os.path import getsize
from django_cron import CronJobBase, Schedule
from Servus.settings import BASE_DIR, STATIC_URL
from Servus.Servus import SLIDESHOW_EXCLUDE_DIRS
from base.models import Slideshow, MTime


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

    def do(self):    
        """
        Очистка базы base_slideshow перед заполнением свежими данными 
        """ 
        
        from time import time
        t1 = time()
        
        path_to_imgs = '%s%simg/slideshow' % (BASE_DIR.replace('\\', '/'), STATIC_URL) 
        mtime = stat(path_to_imgs).st_mtime
        dir_changed = False
        try:                
            if mtime != MTime.objects.get(id=1):
                MTime.objects.all().delete()
                try:
                    Slideshow.objects.all().delete()
                except Slideshow.DoesNotExist:
                    pass
                dir_changed = True
        except MTime.DoesNotExist:
            dir_changed = True
        
        if dir_changed:
            obj_mt = MTime.objects.create(mtime = mtime)
            obj_mt.save()            
            for root, dirs, files in walk(unicode(path_to_imgs), followlinks=True):   
    
                # Изменение списка 'dirnames' остановит обход папок os.walk().
                for exclude_folder in SLIDESHOW_EXCLUDE_DIRS:
                    if exclude_folder in dirs:
                        dirs.remove(exclude_folder) 
                    
                amount_files = len(files)
                if amount_files:
                    Slideshow.objects.create(album_path = root.replace('\\', '/'))
        print time()- t1