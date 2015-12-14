# coding=utf-8
import smtplib
from urllib2 import urlopen, URLError

from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from base.settings import EMAIL_HOST_USER, SITE_NAME
from base.utils import CJB
from plugins.utils import get_used_plugins_by
from .models import Event
from .utils import event_setter

SERVICECODES = {
    100: u'Сообщение принято к отправке.',
    200: u'Неправильный api_id',
    201: u'Не хватает средств на лицевом счету',
    202: u'Неправильно указан получатель',
    203: u'Нет текста сообщения',
    204: u'Имя отправителя не согласовано с администрацией',
    205: u'Сообщение слишком длинное (превышает 8 СМС)',
    206: u'Будет превышен или уже превышен дневной лимит на отправку сообщений',
    207: u'На этот номер (или один из номеров) нельзя отправлять сообщения, либо указано более 100 номеров\
     в списке получателей',
    208: u'Параметр time указан неправильно',
    209: u'Вы добавили этот номер (или один из номеров) в стоп-лист',
    210: u'Используется GET, где необходимо использовать POST',
    211: u'Метод не найден',
    220: u'Сервис временно недоступен, попробуйте чуть позже.',
    300: u'Неправильный token (возможно истек срок действия, либо ваш IP изменился)',
    301: u'Неправильный пароль, либо пользователь не найден',
    302: u'Пользователь авторизован, но аккаунт не подтвержден (пользователь не ввел код, присланный\
     в регистрационной смс)',
}


class EmailsSendJob(CJB):
    """
    CronJobBase класс для отправки писем с наиболее важными событиями.
    Для отправки используются почтовые настройки, указанные в файле settings.py.
    """

    RUN_EVERY_MINS = 10

    @staticmethod
    def do():
        """
        Функция проверяет наличие сообщений с важностью 'success', 'info', 'warning' и 'error' и
        формирует письмо для отправлки по расписанию на все почтовые адреса из
        таблицы base_userprofile БД. Затем, меняет флаг email_sent у каждого события,
        которое блыо отправлено.
        """

        def email_msg(events):
            """
            :param events: list Список обхектов Event с событиями для формирования сообщения email.
            :returns: tuple Кортеж c текстовыми сообщениями для формирования email
            """

            bgcolors = {1: '#62bd4f', 2: '#3dced8', 3: '#e96506', 4: '#ed4d63'}
            subj = 'Сообщение от %s' % SITE_NAME
            txt_msg = u'\tДата\t\t\tТекст сообщения\n-----------------------------------\n'
            html_msg = u'<table cellpadding=3px><tr><th>Дата</th><th>Текст сообщения</th></tr>'

            for event in events:
                if event.level == 4:
                    subj = 'Важное сообщение от %s' % SITE_NAME

                txt_msg += '%s\t%s\n' % (event.datetime.strftime('%Y.%m.%d %H:%M'), event.message)
                html_msg += '<tr bgcolor=%s><td>%s</font></td><td>%s</td></tr>' \
                            % (bgcolors[event.level], event.datetime.strftime('%Y.%m.%d %H:%M'), event.message)

            html_msg += '</table>'

            return subj, txt_msg, html_msg

        def send_emails(emails, events):
            """
            :param emails: list Список email-адресов получателей.
            :param events: list Список обхектов Event с событиями для формирования сообщения email.
            """

            if events and emails:
                subj, txt_msg, html_msg = email_msg(events)

                try:
                    msg = EmailMultiAlternatives(subj, txt_msg, EMAIL_HOST_USER, emails)
                    msg.attach_alternative(html_msg, 'text/html')
                    msg.send()

                    events.update(email_sent=True)
                except smtplib.SMTPException as err:
                    event_setter('system', u'Ошибка отправки письма: %s' % err, 3, delay=3)

        emails = User.objects.filter(is_active=True).exclude(email='')

        # Список событий и почтовые адреса персонала (is_staff = True),
        #  т.е. тех, кто получает уведомления о системных событиях
        staff_events = Event.objects.filter(level__gte=1).exclude(email_sent=True).order_by('-level')
        staff_emails = emails.exclude(is_staff=False).values_list('email', flat=True)

        # Список событий без системных и почтовые адреса, за исключением адресов персонала (staff)
        events = staff_events.exclude(source='system')
        emails = emails.filter(is_staff=False).values_list('email', flat=True)

        send_emails(staff_emails, staff_events)
        send_emails(emails, events)


class SMSSendJob(CJB):
    """
    CronJobBase класс для отправки SMS-сообщений с наиболее важными событиями.
    Для отправки используются возможность отправки бесплатных сообщений для разработчиков
    на сайте sms.ru.
    """

    RUN_EVERY_MINS = 10

    @staticmethod
    def do():
        """
        Функция проверяет наличие сообщений с важностью 'warning' и 'error' и
        формирует SMS-сообщение для отправлки по расписанию на все api_id из таблицы base_userprofile БД.
        Затем, меняет флаг sms_sent у каждого события, которое
        блыо отправлено.
        """

        recipients = get_used_plugins_by(plugin_type='SMS')
        recipients_filled = [r for r in recipients if r.phone is not None and r.sms_ru_id != '']

        if recipients_filled:
            events = Event.objects.filter(level__gte=3).exclude(sms_sent=True).order_by('-level')

            # Объединяем  все события в одну строку для последующей разбивки по 70 символов
            # (ограничение СМС для русских символов в сообщении)
            txt_msg = '\\n'.join(['[%s] %s' % (e.datetime.strftime('%b-%d %H:%M'), e.message) for e in events])
            sms_msgs = []
            while txt_msg:
                sms_msgs.append(txt_msg[:69])
                txt_msg = txt_msg[69:]

            sms_were_sent = []

            for recipient in recipients_filled:
                for msg in sms_msgs:
                    url = 'http://sms.ru/sms/send?api_id=%s&to=%s&text=%s' % (recipient.sms_ru_id,
                                                                              recipient.phone, msg)
                    # В API sms.ru  в тексте сообщения использутся знаки "+" в качестве пробела
                    url = url.replace(' ', '+')
                    try:
                        res = urlopen(url.encode('utf-8')).read().splitlines()

                        if res is not None and int(res[0]) != 100:
                            event_setter('system', u'Ошибка отправки СМС: %s' % SERVICECODES[int(res[0])], 3, delay=3)
                            sms_were_sent.append(False)
                        else:
                            sms_were_sent.append(True)
                    except URLError as err:
                        event_setter('system', u'Ошибка отправки СМС: %s' % err, 3, delay=3)
                        sms_were_sent.append(False)

            # Если все сообщения отправлены всем получателям, меняем параметр sms_sent сообщений
            if all(sms_were_sent):
                events.update(sms_sent=True)
