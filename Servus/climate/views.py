# coding=utf-8
from base.views import call_template


def climate(request, current_tab):

    params = {}

    return call_template(
        request,
        params,
        current_tab=current_tab
    )