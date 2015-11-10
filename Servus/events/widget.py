# coding=utf-8
from .utils import get_amount_events


def get_widget_data(current_session):
    """
    Функция, выводящая количество и важность событий на Главную страницу в виде виджета.

    :param current_session: str ID текущей сессии браузера, отправившего запрос
    :returns: dict Словарь с количеством и уровнем важности непросмотренных событий.
    """
    
    return get_amount_events(7, session_key=current_session)
