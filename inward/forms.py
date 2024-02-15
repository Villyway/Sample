from datetime import date, datetime

from django import forms

from products.models import Product
from vendors.models import Vendor
from utils.constants import StockTransection

class InWardForm(forms.Form):
    po_no = forms.CharField(required=True, label="Purchase No", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    bill_no = forms.CharField(required=True, label="Invoice/Challan No", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    bill_date = forms.CharField(required=True, label="Invoice/Challan Date", widget=forms.DateInput(
        attrs={"class": "form-control","type":"date"}))
    
    remarks = forms.CharField(required=False, label="Remarks", widget=forms.Textarea(
        attrs={"class": "form-control aiz-text-editor", "rows": "5"}))
    file_url = forms.FileField(required=False, label="Bill PDF", widget=forms.FileInput(attrs={'class': "form-control", 'accept': "PDF"}), help_text="Please upload only .PDF file")
    

    def __init__(self, *args, **kwargs):
        self.user = None
        super(InWardForm, self).__init__(*args, **kwargs)

    def clean_bill_date(self):
        input_date = datetime.strptime(self.cleaned_data.get("bill_date"), '%Y-%m-%d')

        if input_date > datetime.combine(date.today(), datetime.min.time()):
            raise forms.ValidationError('Purchase_Date cannot be in the future.')
        else:
            return input_date 


# Stock
class StockForm(forms.Form):
    part_no = forms.CharField(required="False", label="Part No.", widget=forms.TextInput(
        attrs={"class": "form-control","id":"part-no"}))
    parts = forms.ModelChoiceField(queryset=Product.objects.active(), widget=forms.Select(
        attrs={"class": "form-control form-select","autofocus":True, "id":"parts"}), required=True, label="Part No.", empty_label='--- Select Product ---')
    transection_type = forms.ChoiceField(required=True, label="Transection Type", choices=StockTransection.choices(
    ), widget=forms.Select(attrs={"class": "form-control form-select"}))
    receive_by = forms.CharField(required=True, label="Receive By", widget=forms.TextInput(
        attrs={"class": "form-control"}))
    qty = forms.CharField(required=True, label="Issued Qty", widget=forms.NumberInput(
        attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        self.user = None
        super(StockForm, self).__init__(*args, **kwargs)