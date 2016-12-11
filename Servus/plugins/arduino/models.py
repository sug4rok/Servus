# coding=utf-8
import time
from datetime import datetime
import logging
import serial

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

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
    master = models.ForeignKey(
        'self',
        related_name='arduino_master',
        verbose_name='Основной контроллер',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    port = models.CharField(
        default=1,
        max_length=20,
        verbose_name='Serial-порт',
        help_text='Serial-порт, к которому подключен контроллер. Например:<br>\
                  для Windows порт = № порта - 1;<br>\
                  для Linux   порт = /dev/ttyACM0<br>\
                  Если выбран основной контроллер, выбираем номер UART, к которому подключен вторичный контроллер\
                  (для mega2560 это 1, 2 или 3'
    )

    class Meta(object):
        verbose_name = 'Контроллер Arduino'
        verbose_name_plural = 'Контроллеры Arduino'

    def __unicode__(self):
        return '%s: %s' % (self.name, self.port)

    state = (True, '')
    ser = None

    def perform_commands(self):
        """
        Запуска на выполнение всех невыполненных заданий для данного контроллера
        (объекты класса Command, где контроллер - текущий контроллер и параметр
        is_done = False).
        """

        commands = Command.objects.filter(controller=self, is_done=False)

        if commands:
            self.init_serial()

            if self.state[0]:
                for command in commands:
                    sensor = command.content_object
                    result = self.send(sensor.name, command.command)

                    if result is not None:
                        command.is_done = True
                        command.save()
                        sensor.set_result(result)
            else:
                event_setter('system', self.state[1], 4, delay=3, email=True)
                logger.error(self.state[1])

            self.close_serial()

    def init_serial(self):
        """ Установка соединения с последовательным портом. """

        # Если текущий коннтроллер второстепенный, переменной port назначаем
        # порт основного контроллера.
        if self.master:
            port = self.master.port
        else:
            port = self.port

        try:
            self.ser = serial.Serial(port, 9600, timeout=8)
            time.sleep(2)
        except serial.SerialException:
            self.state = (False, u'Не могу открыть COM-порт %s' % port)

    def send(self, sensor, command):
        """
        Передача команды arduino и возврат полученных от микроконтроллера данных.
        :param sensor: str Наименование датчика. Используется только для логированя ошибок.
        :param command: str Команда arduino. Команда должна быть вида 't10', где
            t - индикатор для скетча arduino, говорящий о том, что далее работа с датчиком
            температуры; 10 - номер вывода (pin) arduino, к которому подключе датчик
        :returns: результат работы переданной arduino команды
        """

        result = None
        if self.state[0] and self.ser is not None:
            if self.ser.isOpen:

                # Если контроллер вторичный, модифицируем пересылаемую команду
                if self.master:
                    command = 'ser%s:%s' % (self.port, command)

                self.ser.write(str(command))
                # time.sleep(1)  # На тестовом макете работало без паузы
                try:
                    result = self.ser.readline()
                    # Отсекаем от результата последние два служебных символа
                    result = result[:-2]
                    if 'Error' in result:
                        self.state = (False,
                                      u'Датчик %s вернул ошибку: %s' % (sensor, result.split('Error: ')[1]))
                        result = None
                    else:
                        self.state = (True, u'OK')
                except Exception as err:
                    self.state = (False, u'Датчик %s: %s' % (sensor, err))
            else:
                self.state = (False, u'COM-порт %s закрыт' % self.port)

        logger.debug('Controller %s: command has been received %s | state: %s ',
                     self, command, self.state[1])

        if self.state[0] is not True:
            event_setter('system', self.state[1], 3, delay=3)
            logger.warning(self.state[1])

        return result

    def close_serial(self):
        """ Завершение работы с последовательным портом. """

        if self.ser is not None:
            self.ser.close()
        self.state = (True, '')


class Command(models.Model):
    """
    Модель для хранения заданий (команд) контроллеров и результатов
    их выполнения.
    """

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    controller = models.ForeignKey(
        Arduino,
        verbose_name='Контроллер Arduino',
    )
    command = models.CharField(
        max_length=50,
        verbose_name='Команда',
    )
    is_done = models.BooleanField(
        default=False,
        verbose_name='Выполнена',
    )
    added = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлена',
    )

    def __unicode__(self):
        return '%s: %s' % (self.controller, self.command)


def is_correct_input_string(string):
    return (type(string) is str or type(string) is unicode) and string != ''


def set_command(sensor, command):
    """
    Функция для упрощения записи заданий контроллеров.
    :param sensor: объект Sensor Модель сенсора.
    :param command: str Команда arduino.
    """

    state = (True, '')
    commands_in_queue = Command.objects.filter(is_done=False).count()

    max_number_commands = 50
    if commands_in_queue < max_number_commands:

        if state[0] and is_correct_input_string(command):
            command_obj, created = Command.objects.get_or_create(object_id=sensor.id,
                                                                 content_type_id=ContentType.objects.get_for_model(
                                                                     sensor).id,
                                                                 controller=sensor.controller,
                                                                 command=command,
                                                                 is_done=False)
        else:
            state = (False, 'Параметр command пустой или неверного типа')

    else:
        state = (False, 'Очередь комманд превысила %s' % max_number_commands)

    if state[0] is not True:
        event_setter('system', state[1], 3, delay=4, email=True)
        logger.error(state[1])
