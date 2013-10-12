# -*- coding: utf_8 -*-
from os import walk
from random import randint
from PIL import Image
from Servus.settings import BASE_DIR, STATIC_URL
from base.views import call_template
from home.models import Slideshow

def home(request):   
    pn, pv = [], []
    
    return call_template(
        request,
        param_names = pn,
        param_vals = pv,
        templ_path = 'base/index.html'
    )
    
def slideshow(request):  
    pn, pv = [], []
    
    pn.append('album')
    pn.append('slide')
    pn.append('slide_width')
    pn.append('slide_height')
        
    path_to_imgs = '%s%simg/slideshow' % (BASE_DIR.replace('\\', '/'), STATIC_URL)
    try:
        latest_id = Slideshow.objects.latest('id').id

        try:
            rnd_id = randint(1, latest_id)
            rnd_album = unicode(Slideshow.objects.get(id=rnd_id).album_path)
            for root, dirs, files in walk(rnd_album):
                rnd_file = randint(0, len(files) - 1)
                slide = '%s/%s' % (rnd_album.replace(path_to_imgs, ''), files[rnd_file])
                img_file = Image.open('%s\%s' % (rnd_album.replace('/', '\\'), files[rnd_file]))
                slide_width, slide_height = img_file.size
                
                pv.append(rnd_album.split('/')[-1])    
                pv.append(slide)
                pv.append(slide_width)
                pv.append(slide_height)
        except IndexError:
            print 'rnd_id:', rnd_id
            print 'rnd_file:', rnd_file
            
    except Slideshow.DoesNotExist:
        pv.append('n/a')
        pv.append('n/a')
    
    return call_template(
        request,
        param_names = pn,
        param_vals = pv,
        templ_path = 'home/slideshow.html'
    )