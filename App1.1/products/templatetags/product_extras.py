from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='adjust_for_pagination')
def adjust_for_counter(value, data):
    value, page = int(value), int(data[0])
    counter_value = value + ((page - 1) * data[1])
    return counter_value