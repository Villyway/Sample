from datetime import date, datetime

from django import forms

from products.models import Product
from vendors.models import Vendor

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

    def __init__(self, *args, **kwargs):
        self.user = None
        super(InWardForm, self).__init__(*args, **kwargs)

    def clean_bill_date(self):
        input_date = datetime.strptime(self.cleaned_data.get("bill_date"), '%Y-%m-%d')

        if input_date > datetime.combine(date.today(), datetime.min.time()):
            raise forms.ValidationError('Purchase_Date cannot be in the future.')
        else:
            return input_date 


#Outword Form
class OutWardForm(forms.Form):
    parts = forms.ModelChoiceField(queryset=Product.objects.active(), widget=forms.Select(
        attrs={"class": "form-control"}), required=True, label="Item", empty_label='--- Select Product ---')    
    issued_qty = forms.CharField(required=True, label="Issued Qty", widget=forms.NumberInput(
        attrs={"class": "form-control"}))
    receive_by = forms.CharField(required=True, label="Receive By", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    remarks = forms.CharField(required=False, label="Remarks", widget=forms.Textarea(
        attrs={"class": "form-control aiz-text-editor", "rows": "5"}))
    



