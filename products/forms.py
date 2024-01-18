from datetime import date, datetime

from django import forms
from django.core.validators import validate_email

from .models import (Unit, Product,
                      Categories, PartQuality, BOMItem  )
from vendors.models import Vendor, PartyType
from utils.models import City, State, Country

class ProductForm(forms.Form):
    code = forms.CharField(required=False,label="Item Code", widget=forms.TextInput(
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
    part_quality = forms.ModelChoiceField(queryset=PartQuality.objects.filter(is_active=True), widget=forms.Select(
        attrs={"class": "form-control form-select"}), required=True, label="Quality", empty_label='--- Select Quality ---')
    part_version = forms.CharField(required=True, label="Item Version", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    image = forms.ImageField(required=False, label="Thumbnail Image(300x 300)",
                                    widget=forms.FileInput(attrs={'class': "form-control", 'accept': "image/jpeg image/png image/jpg",'id':'imgInp'}), help_text="Please upload only .jpg, .jpeg,.png file")

    def __init__(self, *args, **kwargs):
        self.user = None
        self.edit = kwargs.pop("edit", None)
        self.product = kwargs.pop("product", None)
        super(ProductForm, self).__init__(*args, **kwargs)
        if self.edit and self.product:
            self.fields["code"].initial = self.product.code
            self.fields["part_quality"].initial = self.product.quality_type
            self.fields["part_version"].initial = self.product.version
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

    
    # def clean_code(self):
    #     code = self.cleaned_data.get("code")
    #     if self.edit == None:
    #         if Product.objects.filter(code=code):
    #             raise forms.ValidationError(
    #                 "This item code is already registered, please use a different one.")
    #     return code


class BomForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(is_active=True, category__name = "Finish Goods"), widget=forms.Select(
        attrs={"class": "form-control form-select"}), required=True, label="Main Product", empty_label='--- Select Category ---')
    child = forms.ModelChoiceField(queryset=Product.objects.filter(is_active=True), widget=forms.Select(
        attrs={"class": "form-control form-select"}), required=True, label="Child Product", empty_label='--- Select Category ---')
    qty = forms.CharField(label="Quantity", widget=forms.TextInput(
        attrs={"class": "form-control","type":"number","value":"0"}))
    

class FileUploadForm(forms.Form):
    main_part_no = forms.CharField(required=True, label="Main Part No.", widget=forms.TextInput(
        attrs={"class": "form-control m-3"}))
    csv_file = forms.FileField()
    

# Entry of Price and vendor with product table
class VendorWithProduct(forms.Form):    
    comany_name = forms.CharField(required=False, label="Company Name", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    # primary_contect_name = forms.CharField(required=True, label="Primary Contact Name", widget=forms.TextInput(
    #     attrs={"class": "form-control"}))
    # secondary_contect_name = forms.CharField(required=True, label="Secondary Contect Name", widget=forms.TextInput(
    #     attrs={"class": "form-control"}))
    # type = forms.ModelChoiceField(queryset=PartyType.objects.filter(is_active=True), widget=forms.Select(
    #     attrs={"class": "form-control form-select"}), required=False, label="Type", empty_label='--- Select Type ---')
    # mobile = forms.CharField(
    #     required=False, label="Phone/Whatsapp No.", widget=forms.TextInput(attrs={"class": "form-control"}))
    # mobile1 = forms.CharField(
    #     required=False, label="Phone/Whatsapp No.", widget=forms.TextInput(attrs={"class": "form-control"}))
    # email = forms.EmailField(label='Email Address', widget=forms.EmailInput(
    #     attrs={'class': 'form-control'}), required=False, validators=[validate_email])
    # email1 = forms.EmailField(label='Email Address', widget=forms.EmailInput(
    #     attrs={'class': 'form-control'}), required=False, validators=[validate_email])
    # gst_no = forms.CharField(required=True, label="GST No.", widget=forms.TextInput(
    #     attrs={"class": "form-control"}))
    # msme_no = forms.CharField(required=True, label="MSME No.", widget=forms.TextInput(
    #     attrs={"class": "form-control"}))
    # bank_name = forms.CharField(required=True, label="Bank Name", widget=forms.TextInput(
    #     attrs={"class": "form-control"}))
    # bank_branch_name = forms.CharField(required=True, label="Branch Name", widget=forms.TextInput(
    #     attrs={"class": "form-control"}))
    # bank_isfc = forms.CharField(required=True, label="IFSC/MICR Code", widget=forms.TextInput(
    #     attrs={"class": "form-control"}))
    # bank_account_no = forms.CharField(required=True, label="Account No.", widget=forms.TextInput(
    #     attrs={"class": "form-control"}))
    # street = forms.CharField(required=True, label="Street 1",
    #                          widget=forms.TextInput(attrs={"class": "form-control"}))
    # street2 = forms.CharField(required=False, label="Street 2",
    #                           widget=forms.TextInput(attrs={"class": "form-control"}))
    # country = forms.ModelChoiceField(queryset=Country.objects.all(), widget=forms.Select(
    #     attrs={"class": "form-control form-select"}), required=True, label="Country", empty_label='--- Select Country ---')
    # state = forms.ModelChoiceField(queryset=State.objects.all(), widget=forms.Select(
    #     attrs={"class": "form-control form-select"}), required=True, label="State", empty_label='--- Select State ---')
    
    # city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.Select(
    #     attrs={"class": "form-control form-select"}), required=True, label="City", empty_label='--- Select City ---')

    # pincode = forms.IntegerField(required=False, label="Pincode", widget=forms.NumberInput(
    #     attrs={"class": "form-control"}))
    
    product = forms.CharField(required=False, label="Product Of Part No.",
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    price = forms.CharField(required=False, label="Price",
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.active(), widget=forms.Select(
        attrs={"class": "form-control form-select"}), required=False, label="Vendor", empty_label='--- Select Vendor ---')
    