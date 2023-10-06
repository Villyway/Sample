from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='adjust_for_pagination')
def adjust_for_counter(value, page, results_per_page):
    value, page = int(value), int(page)
    counter_value = value + ((page - 1) * results_per_page)
    return counter_value