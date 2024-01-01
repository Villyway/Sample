from django import template
from django.conf import settings

from users.models import User


register = template.Library()

@register.filter(name='adjust_for_pagination')
def adjust_for_counter(value, data):
    value, page = int(value), int(data[0])
    counter_value = value + ((page - 1) * data[1])
    return counter_value


@register.filter(name="get_user")
def get_user_by_id(id):
    return User.objects.single_user(id)
    
        
    
