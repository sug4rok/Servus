# coding=utf-8
from subprocess import Popen, PIPE
from base.utils import CJB
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
                    hdd.set_result(temp)
