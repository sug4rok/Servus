# coding=utf-8
import smtplib
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from Servus.settings import EMAIL_HOST_USER
from Servus.Servus import SITE_NAME
from base.utils import CJB
from events.models import Event


class EmailsSendJob(CJB):
    """
    CronJobBase класс для отправки писем с наиболее важными событиями.
    Для отправки используются почтовые настройки, указанные в файле settings.py.
    """

    RUN_EVERY_MINS = 10

    @staticmethod
    def do():
        """
        Функция проверяет наличие сообщений с важностью 'warning' и 'error' и
        формирует письмо для отправлки по расписанию на все почтовые адреса из
        таблицы auth_user БД. Затем, меняет флаг was_sent у каждого события, которое
        блыо отправлено.
        """

        events = Event.objects.filter(event_imp__gte=3).exclude(was_sent=True).order_by('-event_imp')
        emails = User.objects.exclude(email='').values_list('email', flat=True)

        subj = 'Предупреждение от %s' % SITE_NAME

        txt_msg = u'\tДата\t\t\tТекст сообщения\n'
        txt_msg += '-----------------------------------\n'

        html_msg = u'<table cellpadding=3px><tr><th>Дата</th><th>Текст сообщения</th></tr>'

        for e in events:
            bgcolor = '#faebcc'

            if e.event_imp == 4:
                bgcolor = '#ebccd1'
                subj = 'Важное сообщение от %s' % SITE_NAME

            txt_msg += '%s\t%s\n' % (e.event_datetime.strftime('%Y.%m.%d %H:%M'), e.event_descr)
            html_msg += '<tr bgcolor=%s><td>%s</font></td><td>%s</td></tr>' \
                        % (bgcolor, e.event_datetime.strftime('%Y.%m.%d %H:%M'), e.event_descr)

        html_msg += '</table>'

        if events and emails:
            try:
                msg = EmailMultiAlternatives(subj, txt_msg, EMAIL_HOST_USER, emails)
                msg.attach_alternative(html_msg, 'text/html')
                msg.send()

                events.update(was_sent=True)
            except smtplib.SMTPException as e:
                print e