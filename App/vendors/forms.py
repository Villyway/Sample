from django import forms
from django.core.validators import validate_email
from django.core.validators import RegexValidator

from utils.models import Address, State, City, Country
from .models import Vendor

class VendorForm(forms.Form):
    mobile_regex = RegexValidator(
        regex=r'^[6-9][0-9]{9}', message="Mobile number must be entered with code in the format: 9999999999. It must start with 6, 7, 8, 9")
    # code = forms.CharField(required=True, label="Vendor Code", widget=forms.TextInput(
    #     attrs={"class": "form-control"}))
    name = forms.CharField(required=True, label="Vendor Name", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    mobile = forms.CharField(
        required=False, max_length=10, label=" Vendor Mobile", widget=forms.NumberInput(attrs={"class": "form-control", "type": "tel"}), validators=[mobile_regex])
    email = forms.EmailField(label='Vendor Email', widget=forms.EmailInput(
        attrs={'class': 'form-control'}), required=False, validators=[validate_email])
    gst_no = forms.CharField(required=True, label="GST No.", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    street = forms.CharField(required=True, label="Street 1",
                             widget=forms.TextInput(attrs={"class": "form-control"}))
    street2 = forms.CharField(required=False, label="Street 2",
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    country = forms.ModelChoiceField(queryset=Country.objects.all(), widget=forms.Select(
        attrs={"class": "form-control"}), required=True, label="Country", empty_label='--- Select Country ---')
    state = forms.ModelChoiceField(queryset=State.objects.all(), widget=forms.Select(
        attrs={"class": "form-control"}), required=True, label="State", empty_label='--- Select State ---')
    
    city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.Select(
        attrs={"class": "form-control"}), required=True, label="City", empty_label='--- Select City ---')

    pincode = forms.IntegerField(required=False, label="Pincode", widget=forms.NumberInput(
        attrs={"class": "form-control"}))
    
    def __init__(self, *args, **kwargs):
        self.user = None
        self.edit = kwargs.pop("edit", None)
        self.vendor = kwargs.pop("vendor", None)
        
        super(VendorForm, self).__init__(*args, **kwargs)
        if self.edit and self.vendor:
            self.address = self.vendor.address.first()
            # self.fields["code"].initial = self.vendor.code
            # self.fields['code'].widget.attrs['readonly'] = True
            self.fields["name"].initial = self.vendor.name
            self.fields["mobile"].initial = self.vendor.mobile
            self.fields["email"].initial = self.vendor.email
            self.fields["gst_no"].initial = self.vendor.gst_no
            self.fields["street"].initial = self.address.street
            self.fields["street2"].initial =self.address.street2
            self.fields["country"].initial =self.address.country
            self.fields["state"].initial = self.address.state
            self.fields["city"].initial = self.address.city
            self.fields["pincode"].initial =self.address.zip
    
    def clean_gst_no(self):
        try:
            if Vendor.objects.get(gst_no=self.cleaned_data.get("gst_no")):
                raise forms.ValidationError(
                        "This Vendor is Already registerd.")
        except:
            pass

    

class AddressForm(forms.Form):
    street = forms.CharField(required=True, label="Street 1",
                             widget=forms.TextInput(attrs={"class": "form-control"}))

    street2 = forms.CharField(required=False, label="Street 2",
                              widget=forms.TextInput(attrs={"class": "form-control"}))

    city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.Select(
        attrs={"class": "form-control"}), required=True, label="City", empty_label='--- Select City ---')

    state = forms.ModelChoiceField(queryset=State.objects.all(), widget=forms.Select(
        attrs={"class": "form-control"}), required=True, label="State", empty_label='--- Select State ---')

    country = forms.ModelChoiceField(queryset=Country.objects.all(), widget=forms.Select(
        attrs={"class": "form-control"}), required=True, label="Country", empty_label='--- Select Country ---')

    pincode = forms.IntegerField(required=False, label="Pincode", widget=forms.NumberInput(
        attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        self.edit = kwargs.pop("edit", None)
        self.address = kwargs.pop("address", None)
        super(AddressForm, self).__init__(*args, **kwargs)
        if self.edit and self.address:
            self.fields["street"].initial = self.address.street
            self.fields["street2"].initial = self.address.street2
            self.fields["city"].initial = self.address.city
            self.fields["state"].initial = self.address.state
            self.fields["country"].initial = self.address.country
            self.fields["pincode"].initial = self.address.zip
