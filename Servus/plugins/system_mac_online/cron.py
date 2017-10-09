# coding=utf-8
from multiprocessing.dummy import Pool

from base.utils import CJB
from plugins.utils import get_plugins_by_package
from events.utils import event_setter
from .utils import get_mac, current_ip, pool_ips

MACAddress = get_plugins_by_package(package='plugins.system_mac_online')[0]


def set_mac_status(mac, status):
    mac_obj, created = MACAddress.objects.get_or_create(mac=mac)

    if mac_obj.online != status:
        mac_obj.online = status
        mac_obj.save()
    if created:
        mac_obj.name = 'unknown'
        mac_obj.online = status
        mac_obj.is_used = True
        mac_obj.save()
        event_setter('system', u'Появился новый MAC-адрес: {0}'.format(mac), 2, email=False, delay=4)



class GetMACOnline(CJB):
    """
    CronJobBase класс для ping'а сетевых устройств и записи их доступности.
    """

    RUN_EVERY_MINS = 1

    def do(self):
        ips = pool_ips(1, 255, current_ip())

        pool = Pool(13)  # for me 13 threads is optimally
        macs_online = pool.map(get_mac, ips)
        macs_online = filter(lambda item: item is not None, macs_online)
        pool.close()
        pool.join()

        for mac in macs_online:
            set_mac_status(mac, True)

        macs_db = MACAddress.objects.values_list('mac', flat=True)
        for mac in macs_db:
            if mac not in macs_online:
                set_mac_status(mac, False)
