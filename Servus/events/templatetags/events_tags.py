# coding=utf-8
from django.template.defaulttags import register


@register.filter
def get_alert(dictionary, key):
    return dictionary.get(key)
