# coding=utf-8
import time
import serial
import logging

logger = logging.getLogger(__name__)


class Controller(object):
    """
    Класс для работы с контроллером arduino, подключенного к последовательному порту.
    """
    
    def __init__(self, obj):
        """
        Инициализация подключения к последовательному порту. Проверяем наличие у передаваемого
        объекта атрибута controller и пытаемся подключиться к порту, указанному в controller.port.
        
        :param obj: object Объект, подключенный к порту port
        """
        
        self.obj = obj
        self.state = (True, '')
        
        try:
            self.port = obj.controller.port
            
            try:
                self.ser = serial.Serial(self.port)
                time.sleep(2)
            except serial.SerialException:
                self.state = (False, u'Не могу открыть COM-порт %s' % self.port)
                
        except AttributeError:
            self.state = (False, u'Передаваемый контроллеру объект %s не имеет атрибута controller' % self.obj)

    def command(self, cmd):
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
                        logger.warning(u'Датчик %s вернул неверные данные' % self.obj.name)
                        self.state = (False, 'Датчик вернул данные с ошибкой')
                    else:
                        self.state = (True, 'OK')
                except:
                    self.state = (False, u'Ошибка получения данных')
            else:
                self.state = (False, u'COM-порт %s закрыт' % self.port)
        return result
    
    def close_port(self):
        """
        Завершение работы с последовательным портом
        """
        
        self.ser.close()
