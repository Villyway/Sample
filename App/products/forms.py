from datetime import date, datetime

from django import forms

from .models import (Unit, Product, Attribute,
                     ProductAttribute, )
from vendors.models import Vendor

class ProductForm(forms.Form):
    code = forms.CharField(required=True, label="Item Code", widget=forms.TextInput(
        attrs={"class": "form-control"}))    
    name = forms.CharField(required=True, label="Item Name", widget=forms.TextInput(
        attrs={"class": "form-control"}))    
    umo = forms.ModelChoiceField(queryset=Unit.objects.all(), widget=forms.Select(
        attrs={"class": "form-control"}), required=True, label="Unit", empty_label='--- Select Unit ---')    
    stock = forms.CharField(required=False, label="Stock", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    minimum_stock_level = forms.CharField(required=False, label="Minimum Stock Level", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    rack_no = forms.CharField(required=False, label="Rack No", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    tray_no = forms.CharField(required=False, label="Tray No", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    description = forms.CharField(required=False, label="Description", widget=forms.Textarea(
        attrs={"class": "form-control aiz-text-editor", "rows": "5"}))
    specification = forms.CharField(required=False, label="Specification", widget=forms.Textarea(
        attrs={"class": "form-control aiz-text-editor", "rows": "5"}))    
    image = forms.ImageField(required=False, label="Thumbnail Image(300x 300)",
                                    widget=forms.FileInput(attrs={'class': "form-control", 'accept': "image/jpeg image/png image/jpg"}), help_text="Please upload only .jpg, .jpeg,.png file")

    def __init__(self, *args, **kwargs):
        self.user = None
        self.edit = kwargs.pop("edit", None)
        self.product = kwargs.pop("product", None)
        super(ProductForm, self).__init__(*args, **kwargs)
        if self.edit and self.product:
            self.fields["code"].initial = self.product.code
            self.fields["name"].initial = self.product.name
            self.fields['code'].widget.attrs['readonly'] = True
            self.fields["description"].initial = self.product.description
            self.fields["umo"].initial = self.product.umo
            self.fields["specification"].initial = self.product.specification
            self.fields["stock"].initial = self.product.stock
            self.fields["minimum_stock_level"].initial = self.product.minimum_stock_level
            self.fields["rack_no"].initial = self.product.rack_no
            self.fields["tray_no"].initial = self.product.tray_no
            self.fields["image"].initial = self.product.image
            

