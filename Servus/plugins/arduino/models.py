﻿# coding=utf-8
import time
import logging

import serial
from django.db import models

from events.utils import event_setter

logger = logging.getLogger(__name__)

MODEL = 'Arduino'


class Arduino(models.Model):
    """
    Модель для описания подключенного контроллера Arduino
    """

    CONTAINER = 'system'
    TYPE = 'Controller'

    name = models.CharField(
        max_length=50,
        verbose_name='Модель',
        unique=True
    )
    port = models.CharField(
        default=1,
        max_length=20,
        verbose_name='COM-порт',
        help_text='COM-порт, к которому подключен контроллер.<br>\
                  Например:<br>\
                  В Windows порт = № порта - 1;<br>\
                  В Linux   порт = /dev/ttyACM0'
    )

    class Meta(object):
        verbose_name = 'Контроллер Arduino'
        verbose_name_plural = 'Контроллеры Arduino'

    def __unicode__(self):
        return '%s: %s' % (self.name, self.port)

    class Command(object):
        """
        Класс для работы с контроллером arduino, подключенного к последовательному порту.
        """

        def __init__(self, obj):
            """
            Инициализация подключения к последовательному порту. Пытаемся подключиться к порту для
            дальнейшей передачи комманды.

            :param obj: object Объект, подключенный к данному контроллеру (датчик, сервопривод и пр.).
            """

            self.state = (True, '')
            self.obj = obj

            try:
                self.port = obj.controller.port

                try:
                    self.ser = serial.Serial(self.port)
                    time.sleep(2)
                except serial.SerialException:
                    self.state = (False, u'Не могу открыть COM-порт %s' % self.port)

            except AttributeError:
                self.state = (False, u'Переданный контроллеру объект %s не имеет атрибута port' % self.obj)

            if self.state[0] is not True:
                event_setter('system', self.state[1], 4, delay=3, email=True)
                logger.error(self.state[1])

        def send(self, cmd):
            """
            Передача команды arduino и запись возвращаемых от нее результатов.
            :param cmd: str Команда arduino. Команда должна быть на данном этапе вида 't10',
            где t - индикатор для скетча arduino, говорящий о том, что далее работа с датчиком
            температуры; 10 - номер вывода (pin) arduino, к которому подключе датчик
            :returns: результат работы переданной arduino команды
            """

            result = ''

            if self.state[0]:
                if self.ser.isOpen:
                    self.ser.write(cmd)
                    time.sleep(1)
                    try:
                        result = self.ser.readline()
                        # Отсекаем от результата последние два служебных символа
                        result = result[:-2]
                        if 'e' in result:
                            self.state = (False, u'Датчик %s вернул неверные данные' % self.obj.name)
                        else:
                            self.state = (True, u'OK')
                    except Exception as err:
                        self.state = (False, u'Датчик %s: %s' % (self.obj.name, err))
                else:
                    self.state = (False, u'COM-порт %s закрыт' % self.port)

            logger.debug('Controller %s: command has been received %s | result %s | state: %s ',
                         self.obj.controller, cmd, result, self.state[1])

            if self.state[0] is not True:
                event_setter('system', self.state[1], 3, delay=3)
                logger.warning(self.state[1])

            return result

        def close_port(self):
            """
            Завершение работы с последовательным портом
            """

            self.ser.close()
