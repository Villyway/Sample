from datetime import date, datetime

from django import forms

from .models import (Unit, Product, Attribute,
                     ProductAttribute, Categories )
from vendors.models import Vendor

class ProductForm(forms.Form):
    code = forms.CharField(required=True, label="Item Code", widget=forms.TextInput(
        attrs={"class": "form-control"}))    
    name = forms.CharField(required=True, label="Item Name", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    category = forms.ModelChoiceField(queryset=Categories.objects.filter(is_active=True), widget=forms.Select(
        attrs={"class": "form-control form-select"}), required=True, label="Category", empty_label='--- Select Category ---')
    umo = forms.ModelChoiceField(queryset=Unit.objects.all(), widget=forms.Select(
        attrs={"class": "form-control form-select"}), required=True, label="Unit", empty_label='--- Select Unit ---')    
    stock = forms.CharField(required=False, label="Stock", widget=forms.TextInput(
        attrs={"class": "form-control"}), initial=0)
    minimum_stock_level = forms.CharField(required=False, label="Minimum Stock Level", widget=forms.TextInput(
        attrs={"class": "form-control"}), initial=0)
    rack_no = forms.CharField(required=False, label="Rack No", widget=forms.TextInput(
        attrs={"class": "form-control"}), initial=0)
    tray_no = forms.CharField(required=False, label="Tray No", widget=forms.TextInput(
        attrs={"class": "form-control"}),initial=0)
    description = forms.CharField(required=False, label="Description", widget=forms.Textarea(
        attrs={"class": "form-control aiz-text-editor", "rows": "5"}))
    specification = forms.CharField(required=False, label="Specification", widget=forms.Textarea(
        attrs={"class": "form-control aiz-text-editor", "rows": "5"}))    
    image = forms.ImageField(required=False, label="Thumbnail Image(300x 300)",
                                    widget=forms.FileInput(attrs={'class': "form-control", 'accept': "image/jpeg image/png image/jpg",'id':'imgInp'}), help_text="Please upload only .jpg, .jpeg,.png file")

    def __init__(self, *args, **kwargs):
        self.user = None
        self.edit = kwargs.pop("edit", None)
        self.product = kwargs.pop("product", None)
        super(ProductForm, self).__init__(*args, **kwargs)
        if self.edit and self.product:
            self.fields["code"].initial = self.product.code
            self.fields["name"].initial = self.product.name
            self.fields["category"].initial = self.product.category
            self.fields['code'].widget.attrs['readonly'] = True
            self.fields["description"].initial = self.product.description
            self.fields["umo"].initial = self.product.umo
            self.fields["specification"].initial = self.product.specification
            self.fields["stock"].initial = self.product.stock
            self.fields["minimum_stock_level"].initial = self.product.minimum_stock_level
            self.fields["rack_no"].initial = self.product.rack_no
            self.fields["tray_no"].initial = self.product.tray_no
            self.fields["image"].initial = None

    
    def clean_code(self):
        code = self.cleaned_data.get("code")
        if self.edit == None:
            if Product.objects.filter(code=code):
                raise forms.ValidationError(
                    "This item code is already registered, please use a different one.")

        return code
            

