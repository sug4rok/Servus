# coding=utf-8
import time
import serial
try:
    from base.settings import PORT
except ImportError:
    PORT = '/dev/ttyACM0'


class Arduino(object):
    """
    Класс для работы с контроллером arduino, подключенного к последовательному порту.
    """
    
    def __init__(self, port=PORT):
        """
        Инициализация подключения к последовательному порту.
        :param port: str Обязательный параметр номер (имя порта)
        """
        
        self.port = port
        self.state = (True, '')
        try:
            self.ser = serial.Serial(self.port)
            time.sleep(2)
        except serial.SerialException:
            self.state = (False, u'Не могу открыть COM-порт %s' % self.port)

    def command(self, cmd):
        """
        Передача команды arduino и запись возвращаемых от нее результатов.
        :param cmd: str Команда arduino. Команда должна быть на данном этапе вида 't10',
        где t - индикатор для скетча arduino, говорящий о том, что далее работа с датчиком
        температуры; 10 - номер вывода (pin) arduino, к которому подключе датчик
        :returns: результат работы переданной arduino команды
        """
        
        result = ''
        if self.ser.isOpen:
            self.ser.write(cmd)
            time.sleep(1)
            try:
                result = self.ser.readline()
                # Отсекаем от результата последние два служебных символа
                result = result[:-2]
                if 'e' in result:
                    logger.warning(u'Датчик %s вернул неверные данные' % s)
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