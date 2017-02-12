# coding=utf-8
from multiprocessing.dummy import Pool

from base.utils import CJB
from events.utils import event_setter
from plugins.utils import get_used_plugins_by
from .utils import triple_ping


def set_host_status(host):
    result = triple_ping(host.ip_address)
    if host.online != result:
        host.online = result
        host.save()

        msg = u'%s %s' % (host.name, u'снова доступен' if result else u'больше не доступен')
        if result:
            event_setter('system', msg, 1, email=True, delay=1)
        else:
            event_setter('system', msg, 3, email=True, delay=1)


class GetIPOnline(CJB):
    """
    CronJobBase класс для ping'а сетевых устройств и записи их доступности.
    """

    RUN_EVERY_MINS = 1

    def do(self):

        hosts = get_used_plugins_by(package='plugins.system_ip_online')

        if hosts:
            pool = Pool(5)  # 5 - количество потоков
            pool.map(set_host_status, hosts)
            pool.close()
            pool.join()
