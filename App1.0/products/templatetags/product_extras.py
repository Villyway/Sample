from django import template
from django.conf import settings

register = template.Library()

@register.filter
def adjust_for_counter(value, page):
    value, page = int(value), int(page)
    counter_value = value + ((page - 1) * settings.RESULTS_PER_PAGE)
    return counter_value