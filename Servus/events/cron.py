# coding=utf-8
import smtplib
from urllib2 import urlopen, URLError
from django.core.mail import EmailMultiAlternatives
from Servus.settings import EMAIL_HOST_USER
from Servus.Servus import SITE_NAME
from base.models import UserProfile
from base.utils import CJB
from events.models import Event
from events.utils import event_setter

servicecodes = {
    100: 'Сообщение принято к отправке.',
    200: 'Неправильный api_id',
    201: 'Не хватает средств на лицевом счету',
    202: 'Неправильно указан получатель',
    203: 'Нет текста сообщения',
    204: 'Имя отправителя не согласовано с администрацией',
    205: 'Сообщение слишком длинное (превышает 8 СМС)',
    206: 'Будет превышен или уже превышен дневной лимит на отправку сообщений',
    207: 'На этот номер (или один из номеров) нельзя отправлять сообщения, либо указано более 100 номеров в списке получателей',
    208: 'Параметр time указан неправильно',
    209: 'Вы добавили этот номер (или один из номеров) в стоп-лист',
    210: 'Используется GET, где необходимо использовать POST',
    211: 'Метод не найден',
    220: 'Сервис временно недоступен, попробуйте чуть позже.',
    300: 'Неправильный token (возможно истек срок действия, либо ваш IP изменился)',
    301: 'Неправильный пароль, либо пользователь не найден',
    302: 'Пользователь авторизован, но аккаунт не подтвержден (пользователь не ввел код, присланный в регистрационной смс)',
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
        Функция проверяет наличие сообщений с важностью 'warning' и 'error' и
        формирует письмо для отправлки по расписанию на все почтовые адреса из
        таблицы base_userprofile БД. Затем, меняет флаг email_sent у каждого события,
        которое блыо отправлено.
        """

        events = Event.objects.filter(event_imp__gte=3).exclude(email_sent=True).order_by('-event_imp')
        emails = UserProfile.objects.exclude(email='').values_list('email', flat=True)

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

                events.update(email_sent=True)
            except smtplib.SMTPException as e:
                event_setter('system', 'Ошибка отправки письма: %s' % e, 3, delay=3)


class SMSSendJob(CJB):
    """
    CronJobBase класс для отправки SMS-сообщений с наиболее важными событиями.
    Для отправки используются возможность отправки бесплатных сообщений для разработчиков
    на сайте sms.ru. Затем, меняет флаг sms_sent у каждого события,
    которое блыо отправлено.
    """

    RUN_EVERY_MINS = 10

    @staticmethod
    def do():
        """
        Функция проверяет наличие сообщений с важностью 'warning' и 'error' и
        формирует SMS-сообщение для отправлки по расписанию на все api_id из таблицы base_userprofile БД.
        Затем, меняет флаг email_sent у каждого события, которое
        блыо отправлено.
        """

        events = Event.objects.filter(event_imp__gte=3).exclude(sms_sent=True).order_by('-event_imp')
        recipients = UserProfile.objects.exclude(sms_ru_id='').values().exclude(phone=None)

        txt_msg = ''

        if recipients:
            for r in recipients:
                for e in events:
                    txt_msg = '[%s] %s' % (e.event_datetime.strftime('%b-%d %H:%M'), e.event_descr)
                    url = 'http://sms.ru/sms/send?api_id=%s&to=%s&text=%s' % (r['sms_ru_id'], r['phone'], txt_msg)
                    # В API sms.ru  в тексте сообщения использутся знаки "+" в качестве пробела
                    url = url.replace(' ', '+')
                    try:
                        res = urlopen(url.encode('utf-8')).read().splitlines()

                        if res is not None and int(res[0]) != 100:
                            event_setter('system', 'Ошибка отправки СМС: %s' % servicecodes[int(res[0])], 3, delay=3)
                        else:
                            e.sms_sent = True
                            e.save()
                    except URLError as e:
                        event_setter('system', 'Ошибка отправки СМС: %s' % e, 3, delay=3)