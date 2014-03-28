﻿# coding=utf-8
from os import walk, stat
import smtplib
import time
from datetime import datetime, timedelta
import serial
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django_cron import CronJobBase, Schedule
from Servus.settings import EMAIL_HOST_USER
from Servus.Servus import SITE_NAME, SLIDESHOW_ROOT, PORT
from base.models import Event, Slideshow, SlideshowChanges
from climate.models import TempHumidSensor, TempHumidValue


class EmailsSendJob(CronJobBase):
    """
    Class to send emails with important events
    """

    RUN_EVERY_MINS = 10
    RETRY_AFTER_FAILURE_MINS = 5
    # RUN_AT_TIMES = ['04:00']

    schedule = Schedule(
        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS,
        # run_at_times=RUN_AT_TIMES
        run_every_mins=RUN_EVERY_MINS
    )
    code = 'EmailsSendJob'    # a unique code

    @staticmethod
    def do():
        """
        Функция проверяет наличие сообщений с важностью 'warning' и 'error' и
        формирует письмо для отправлки по расписанию на все почтовые адреса из
        таблицы auth_user БД. Затем, меняет флаг was_sent у каждого события, которое
        блыо отправлено.
        """

        events = Event.objects.filter(event_imp__gte=3).exclude(was_sent=True)
        emails = User.objects.exclude(email='').values_list('email', flat=True)
        subj = 'Предупреждение от %s' % SITE_NAME
        txt_mes = u'\tДата\t\t\tТекст сообщения\n'
        txt_mes += '-----------------------------------\n'
        for e in events:
            if e.event_imp == 4:
                subj = 'Важное сообщение от %s' % SITE_NAME
            txt_mes += '%s\t%s\n' % (e.event_datetime.strftime('%Y.%m.%d %H:%M'), e.event_descr)
        if events and emails:
            try:
                send_mail(subj, txt_mes, EMAIL_HOST_USER, emails)
                events.update(was_sent=True)
            except smtplib.SMTPException as e:
                print e


class SlideshowJob(CronJobBase):
    # RUN_EVERY_MINS = 60
    RETRY_AFTER_FAILURE_MINS = 5
    RUN_AT_TIMES = ['04:00']
    
    schedule = Schedule(
        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS,
        run_at_times=RUN_AT_TIMES
        # run_every_mins=RUN_EVERY_MINS
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


class GetSensorsValues(CronJobBase):
    """
    This class for obtaining the temperature and humidy values
    """

    RUN_EVERY_MINS = 15
    RETRY_AFTER_FAILURE_MINS = 5
    # RUN_AT_TIMES = ['04:00']

    schedule = Schedule(
        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS,
        # run_at_times=RUN_AT_TIMES
        run_every_mins=RUN_EVERY_MINS
    )
    code = 'GetSensorsValues'    # a unique code

    @staticmethod
    def do():
        sensors = TempHumidSensor.objects.filter(is_used=True)
        if sensors:
            try:
                ser = serial.Serial(PORT)
                if ser.isOpen:
                    for s in sensors:
                        ser.flushInput()  # flush input buffer, discarding all its contents
                        ser.flushOutput()  # flush output buffer, aborting current output

                        ser.write('t%s\n' % s.sensor_pin)
                        time.sleep(1)
                        ser_out = ser.readline()[:-2].split(':')

                        if ser_out[0] != 'e' and ser_out[1] != 'e':
                            TempHumidValue.objects.create(
                                sensor_name=s,
                                temperature=ser_out[1],
                                humidity=ser_out[0]
                            )
                        else:
                            event_setter('climate', u'Ошибка получения данных с %s' % s.sensor_name, 0)

                    ser.close()
            except serial.serialutil.SerialException:
                event_setter('climate', u'Не могу открыть порт COM%s' % PORT, 3)


def event_setter(event_src, event_descr, event_imp):
    """
    Функция записи новых сообщений в БД (таблица base_event).
    В БД записываются только уникальные (сравнение event_descr) в пределах суток сообщения.
    На входе:
        events_src - источник события;
        event_descr - описание события (сообщение);
        event_imp - важность (от 0 до 4)
    """

    events = Event.objects.filter(event_datetime__gte=datetime.now() - timedelta(days=1))

    if event_descr not in events.values_list('event_descr', flat=True):
        Event.objects.create(event_src=event_src, event_descr=event_descr, event_imp=event_imp)