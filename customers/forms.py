from django import forms
from django.core.validators import validate_email
from django.core.validators import RegexValidator

from utils.models import State, City, Country
from .models import Customer
from utils.constants import OrdersType

class CustomerForm(forms.Form):
    mobile_regex = RegexValidator(
        regex=r'^[6-9][0-9]{9}', message="Mobile number must be entered with code in the format: 9999999999. It must start with 6, 7, 8, 9")
    category = forms.ChoiceField(required=True, label="Customer Type", choices=OrdersType.choices(
    ), widget=forms.Select(attrs={"class": "form-control form-select"}))
    name = forms.CharField(label="Customer", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    person_name = forms.CharField(label="Contect Person Name", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    mobile1 = forms.CharField(
        required= True ,label=" Mobile No", widget=forms.TextInput(attrs={"class": "form-control"}))
    mobile2 = forms.CharField(
        label=" Alternative Mobile No", widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-control'}), required=False, validators=[validate_email])
    gst_no = forms.CharField(
        required= False ,label=" GST No", widget=forms.TextInput(attrs={"class": "form-control"}))
    
    
    
    def __init__(self, *args, **kwargs):
        self.user = None
        self.edit = kwargs.pop("edit", None)
        self.customer = kwargs.pop("customer", None)
        
        super(CustomerForm, self).__init__(*args, **kwargs)
        if self.edit and self.customer:
            self.fields['name'].initial = self.customer.name
            self.fields["person_name"].initial = self.customer.contect_person
            self.fields['mobile1'].initial = self.customer.mobile
            self.fields["mobile2"].initial = self.customer.mobile1
            self.fields["email"].initial = self.customer.email
            self.fields["gst_no"].initial = self.customer.gst_no
            
    

class CustomerAddressDetails(forms.Form):
    person_name = forms.CharField(label="Contect Person Name", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    mobile1 = forms.CharField(
        required= True ,label=" Mobile No", widget=forms.TextInput(attrs={"class": "form-control"}))
    street = forms.CharField(required=True, label="Street 1",
                             widget=forms.TextInput(attrs={"class": "form-control"}))
    street2 = forms.CharField(required=False, label="Street 2",
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    country = forms.ModelChoiceField(queryset=Country.objects.all(), widget=forms.Select(
        attrs={"class": "form-control form-select"}), required=True, label="Country", empty_label='--- Select Country ---')
    other_country = forms.CharField(required=False, label="", widget=forms.TextInput(
        attrs={"class": "form-control","placeholder":"Other Country"}))
    state = forms.ModelChoiceField(queryset=State.objects.all(), widget=forms.Select(
        attrs={"class": "form-control form-select"}), required=True, label="State", empty_label='--- Select State ---')
    other_state = forms.CharField(required=False, label="", widget=forms.TextInput(
        attrs={"class": "form-control","placeholder":"Other State"}))
    city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.Select(
        attrs={"class": "form-control form-select"}), required=True, label="City", empty_label='--- Select City ---')
    other_city = forms.CharField(required=False, label="", widget=forms.TextInput(
        attrs={"class": "form-control","placeholder":"Other City"}))
    pincode = forms.IntegerField(required=False, label="Pincode", widget=forms.NumberInput(
        attrs={"class": "form-control"}))
    
    