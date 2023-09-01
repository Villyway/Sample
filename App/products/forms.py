from django import forms

from .models import (Unit, Product, Attribute,
                     ProductAttribute, InWord, Outword)
from vendors.models import Vendor

class ProductForm(forms.Form):
    code = forms.CharField(required=True, label="Item Code", widget=forms.TextInput(
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
            self.fields['code'].widget.attrs['readonly'] = True
            self.fields["description"].initial = self.product.description
            self.fields["umo"].initial = self.product.umo
            self.fields["specification"].initial = self.product.specification
            self.fields["stock"].initial = self.product.stock
            self.fields["minimum_stock_level"].initial = self.product.minimum_stock_level
            self.fields["rack_no"].initial = self.product.rack_no
            self.fields["tray_no"].initial = self.product.tray_no
            self.fields["image"].initial = self.product.image
            

class InWardForm(forms.Form):
    grn_no = forms.CharField(required=True, label="GRN No", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    bill_no = forms.CharField(required=True, label="Bill No", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    bill_date = forms.CharField(required=True, label="Bill Date", widget=forms.DateInput(
        attrs={"class": "form-control","type":"date"}))
    part = forms.ModelChoiceField(queryset=Product.objects.active(), widget=forms.Select(
        attrs={"class": "form-control"}), required=True, label="Item", empty_label='--- Select Product ---')    
    received_qty = forms.CharField(required=True, label="Received Qty", widget=forms.NumberInput(
        attrs={"class": "form-control"}))
    uom = forms.ModelChoiceField(queryset=Unit.objects.all(), widget=forms.Select(
        attrs={"class": "form-control"}), required=True, label="Unit", empty_label='--- Select Unit ---')    
    in_time = forms.CharField(required=True, label="In Time", widget=forms.TimeInput(
        attrs={"class": "form-control", "type":"time"}))
    
    purchase_order_no = forms.CharField(required=True, label="Purchase Order No", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.active(), widget=forms.Select(
        attrs={"class": "form-control"}), required=True, label="Vendor", empty_label='--- Select Vendor ---')    
    receive_by = forms.CharField(required=True, label="Receive By", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    remarks = forms.CharField(required=False, label="Remarks", widget=forms.Textarea(
        attrs={"class": "form-control aiz-text-editor", "rows": "5"}))
    file_url = forms.FileField(required=False, label="Bill PDF", widget=forms.FileInput(attrs={'class': "form-control", 'accept': "PDF"}), help_text="Please upload only .PDF file")
    qc_status = forms.BooleanField(required=False, label="QC", widget=forms.CheckboxInput(attrs={'style': 'width:15px;height:15px;'}))
    

class OutWardForm(forms.Form):
    parts = forms.ModelChoiceField(queryset=Product.objects.active(), widget=forms.Select(
        attrs={"class": "form-control"}), required=True, label="Item", empty_label='--- Select Product ---')    
    issued_qty = forms.CharField(required=True, label="Issued Qty", widget=forms.NumberInput(
        attrs={"class": "form-control"}))
    uom = forms.ModelChoiceField(queryset=Unit.objects.all(), widget=forms.Select(
        attrs={"class": "form-control"}), required=True, label="Unit", empty_label='--- Select Unit ---')    
    # issued_by = forms.CharField(required=True, label="Issued By", widget=forms.TextInput(
    #     attrs={"class": "form-control"}))    
    receive_by = forms.CharField(required=True, label="Receive By", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    remarks = forms.CharField(required=False, label="Remarks", widget=forms.Textarea(
        attrs={"class": "form-control aiz-text-editor", "rows": "5"}))
    



