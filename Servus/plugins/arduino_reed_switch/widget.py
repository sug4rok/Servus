# coding=utf-8
from plugins.utils import get_used_plugins_by


def get_state(state):
    return 'closed' if state else 'opened'


def get_widget_data(plan_id):
    """
    Функция, предоставляющая данные с герконов

    :returns: list Список кортежей с данными о состояниях герконов и
    координатами расположения виджетов.
    """

    switches = get_used_plugins_by(package='plugins.arduino_reed_switch')
    switches = [sw for sw in switches if sw.plan_image_id == plan_id]

    return [(plan_id, sw.name, sw.horiz_position, sw.vert_position,
             sw.level, sw.location_type, get_state(sw.state)) for sw in switches]
