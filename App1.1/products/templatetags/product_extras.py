from django import template
from django.conf import settings

from products.models import Product, VendorWithProductData

register = template.Library()

@register.filter(name='adjust_for_pagination')
def adjust_for_counter(value, data):
    value, page = int(value), int(data[0])
    counter_value = value + ((page - 1) * data[1])
    return counter_value


@register.filter(name='get_price')
def get_price_by_part_no(part_no):
    product = Product.objects.by_part_no(part_no)
    if VendorWithProductData.objects.filter(product = product).exists():
        return VendorWithProductData.objects.filter(product = product).first().price
    return 0


@register.filter(name='get_total_price')
def get_total_price_by_part_no(part_no, qty):
    product = Product.objects.by_part_no(part_no)
    if VendorWithProductData.objects.filter(product = product).exists():
        return VendorWithProductData.objects.filter(product = product).first().price * qty
    return 0
