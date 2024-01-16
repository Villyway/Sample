from django import forms
from django.core.validators import validate_email
from django.core.validators import RegexValidator

from customers.models import Customer
from products.models import Product, Categories
from orders.models import OrderOfProduct
from django.forms import formset_factory

