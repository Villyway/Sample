from django import template
from django.conf import settings

from products.models import Product, VendorWithProductData
from customers.models import Customer

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


@register.filter(name='get_vendor')
def get_vendor_name(part_no):
    product = Product.objects.by_part_no(part_no)
    if VendorWithProductData.objects.filter(product = product).exists():
        return VendorWithProductData.objects.filter(product = product).first().vendor.comany_name
    return "-"


@register.filter(name='get_addresses')
def get_customer_address(customer):
    customer_obj = Customer.objects.get(id = customer)
    if customer_obj.address:
        return customer_obj.address.filter(is_active = True)
    return "-"

@register.filter
def subtract(value, arg):
    if 0 < value - arg:
        return value - arg
    else:
        return 0

@register.filter
def get_requirement(value, arg):
    if 0 > value - arg:
        return value - arg
    else:
        return 0
    

@register.filter
def get_total_of_list(value):
    return sum(list(value))