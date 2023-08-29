from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import View
from django.db import transaction
from django.contrib import messages

from .forms import VendorForm
from .models import Vendor
from utils.models import Address

# Create your views here.
class CreateVendor(FormView):
    form_class = VendorForm
    template_name = "vendors/create.html"

    def form_valid(self, form):
        form_data = form.cleaned_data
        try:
            with transaction.atomic():
                vendor = Vendor.objects.create(
                    code = form_data["code"],
                    name = form_data["name"],
                    mobile = form_data["mobile"],
                    email = form_data["email"],
                    gst_no = form_data["gst_no"],
                    created_by = self.request.user.id

                )
                address = Address()
                address.street = form_data["street"]
                address.street2 = form_data["street2"]
                address.city = form_data["city"]
                address.state = form_data["state"]
                address.country = form_data["country"]
                address.zip = form_data["pincode"]
                address.save()
                vendor.address.add(address)
                address.created_by = self.request.user.id
            return redirect('admin:index')
        
        except Exception as e:
            messages.error(self.request, str(e))
            return redirect("vendors:vendor-create")

