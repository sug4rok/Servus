# coding=utf-8
from plugins.utils import get_used_plugins_by


def get_widget_data(plan_id):
    """
    Функция, предоставляющая данные о температурах HDD

    :returns: list Список кортежей с данными о температурах жестких дистков и
    координатами расположения виджетов.
    """

    switches = get_used_plugins_by(package='plugins.system_hddtemp')
    switches = [sw for sw in switches if sw.plan_image_id == plan_id]

    return [(plan_id, sw.name, sw.horiz_position, sw.vert_position,
             sw.level, sw.temperature) for sw in switches]
