from django import forms
from django.core.validators import validate_email
from django.core.validators import RegexValidator

from customers.models import Customer
from products.models import Product, Categories
from orders.models import OrderOfProduct
from django.forms import formset_factory

class OrdersForm(forms.Form):

    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), widget=forms.Select(
        attrs={"class": "form-control form-select ml-5"}), required=True, label="Customer", empty_label='--- Select Customer ---')
    # product = forms.ModelChoiceField(queryset=Product.objects.finished_product(), widget=forms.Select(
    #     attrs={"class": "form-control form-select ml-5"}), required=True, label="Product", empty_label='--- Select Product ---')
    
