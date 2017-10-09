# coding=utf-8
from subprocess import Popen, PIPE
from base.utils import CJB
from events.utils import event_setter
from plugins.utils import get_used_plugins_by


class GetHDDTemp(CJB):
    """
    CronJobBase класс для определения температуры HDD утилитой hddtemp (linux).
    """

    RUN_EVERY_MINS = 5

    def do(self):

        hdds = get_used_plugins_by(package='plugins.system_hddtemp')

        if hdds:
            for hdd in hdds:
                if hdd.type != '?':
                    hdd_str = '{0}:/dev/{1}'.format(hdd.type, hdd.name)
                else:
                    hdd_str = '/dev/' + hdd.name

                process = Popen(['hddtemp', '-n', hdd_str], stdout=PIPE)
                temp, err = process.communicate()
                temp = temp.replace('\n', '')

                if temp and temp.isdigit():
                    temp = int(temp)
                    hdd.temperature = temp
                    hdd.save()

                    if temp <= 20 or temp >= 50:
                        msg = u'Температура HDD вышла из безопасного диапазона ({0}°C)'.format(temp)
                        event_setter('system', msg, 4, email=True)
                    elif temp <= 25 or temp >= 45:
                        msg = u'Температура HDD близка к критичной ({0}°C)'.format(temp)
                        event_setter('system', msg, 3)
