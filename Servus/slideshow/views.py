﻿# coding=utf-8
from os import walk, path
from random import randint

from PIL import Image
from base.settings import MEDIA_ROOT
from base.views import call_template, amount_events
from .models import Slideshow


class NotImageError(Exception):
    """
    Обработка исключения, возникающего при открытии файлов,
    не являющихся файлми изображений.
    """

    def __init__(self, file_type):
        Exception.__init__(self, file_type)
        self.file_type = file_type

    def __str__(self):
        return repr('NotImageError: type of file is [%s]' % self.file_type)


class PathNotFound(Exception):
    """
    Обработка исключения ошибочного пути до папки с файлми
    изображений.
    """

    def __init__(self, broken_path):
        Exception.__init__(self, broken_path)
        self.broken_path = broken_path

    def __str__(self):
        return repr('PathNotFound: [%s] is not in slideshow directory.' % self.broken_path)


def slideshow(request):
    """
    Функция отображения слайдшоу

    :param request: django request
    """

    return call_template(
        request,
        templ_path='slideshow/slideshow.html'
    )


def slide(request):
    """
    Функция отображения на начальной странице произвольной фотографии

    :param request: django request
    """

    params = {'album': 'Нет альбомов', 'slide': ''}

    albums = Slideshow.objects.exclude(is_shown=False)
    if len(albums):
        slideshow_folder = MEDIA_ROOT + '/slideshow'
        attempts = 0

        # Делаем 10 попыток найти подходящий для показа файл.
        # Если альбом был удален, а база не проиндексирована еще, нет графических файлов,
        # выводим на экран об этом сообщение.
        while attempts < 10:
            try:
                # Получаем первый элемент произвольно отсортированного списка фотоальбомов,
                # исключая альбомы с пометкой is_shown = False
                rnd_album = unicode(
                    slideshow_folder + albums.order_by('?')[0].album_path
                )
                if path.exists(rnd_album):
                    for root, dirs, files in walk(rnd_album):
                        rnd_file = randint(0, len(files) - 1)
                        img = '%s/%s' % (root, files[rnd_file])
                        file_type = img.split('.')[-1].lower()
                        try:
                            Image.open(img)
                            params['album'] = rnd_album.split('/')[-1].replace('_', ' ')
                            params['slide'] = img.replace(MEDIA_ROOT, '').replace('//', '/')
                            break
                        except:
                            raise NotImageError(file_type)
                else:
                    raise PathNotFound(rnd_album)
            except (NotImageError, PathNotFound):
                attempts += 1
                continue
            else:
                break
    return call_template(
        request,
        params,
        templ_path='slideshow/slide.html'
    )


def slideshow_events(request):
    """" Количество непросмотренных событий для отображения на странице слайдшоу """
    return amount_events(request, 'slideshow/slideshow_events.html', days=1)
