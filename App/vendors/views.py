from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import View
from django.db import transaction
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import VendorForm
from .models import Vendor
from utils.models import Address
from utils.views import decode_data



class VendorList(View):
    template_name = "vendors/list.html"

    def get(self, request):
        vendors = Vendor.objects.active()
        page = request.GET.get('page', 1)
        paginator = Paginator(vendors, 10)
        try:
            vendors = paginator.page(page)
        except PageNotAnInteger:
            vendors = paginator.page(1)
        except EmptyPage:
            vendors = paginator.page(paginator.num_pages)
        context = {
            "vendors": vendors,

        }
        return render(request, self.template_name, context)

# Create your views here.
class CreateVendor(FormView):
    form_class = VendorForm
    template_name = "vendors/create.html"

    def form_invalid(self, form):
        super(CreateVendor, self).form_invalid(form)
        messages.error(self.request,form.errors)
        return redirect("vendors:vendor-create")

    def form_valid(self, form):
        form_data = form.cleaned_data
        try:
            with transaction.atomic():
                vendor = Vendor.objects.create(
                    #code = form_data["code"],
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
                messages.success(self.request,"Vendor Successfully created!!")
            return redirect('vendors:vendor-list')
        
        except Exception as e:
            messages.error(self.request, str(e))
            return redirect("vendors:vendor-create")


# vendor Edit
class VendorEditView(FormView):
    form_class = VendorForm
    template_name = "vendors/edit.html"

    def get_form_kwargs(self):
        vendor = Vendor.objects.single_vendor(
            id= self.kwargs["id"])
        kwargs = super(VendorEditView, self).get_form_kwargs()
        kwargs.update({"vendor": vendor, "edit": True})
        return kwargs
    
    def form_valid(self, form):
        form_data = form.cleaned_data
        try:
            with transaction.atomic():
                vendor = Vendor.objects.single_vendor(id = self.kwargs['id'])
                if vendor.name != form_data['name']:
                    vendor.name = form_data['name']
                if vendor.mobile != form_data['mobile']:
                    vendor.mobile = form_data['mobile']
                if vendor.email != form_data['email']:
                    vendor.email = form_data['email']

                if vendor.gst_no != form_data['gst_no']:
                    vendor.gst_no = form_data['gst_no']
                vendor.updated_by = self.request.user.id
                vendor.save()

                address = vendor.address.first()
                if address.street != form_data["street"]:
                    address.street = form_data["street"]
                if address.street2 != form_data["street2"]:
                    address.street2 = form_data["street2"]
                if address.country != form_data["country"]:
                    address.country = form_data["country"]
                if address.state != form_data["state"]:
                    address.state = form_data["state"]
                if address.city != form_data["city"]:
                    address.city = form_data["city"]
                if address.zip != form_data["pincode"]:
                    address.zip = form_data["pincode"]
                address.updated_by = self.request.user.id
                address.save()
                messages.success(self.request,"Vendor Successfully Updated!!")
                return redirect('vendors:vendor-list')
            
        except Exception as e:
            messages.error(self.request, str(e))
            return redirect(self.request.META['HTTP_REFERER'])


class VendorDelete(View):
    
    def get(self,request,id):
        vendor = Vendor.objects.single_vendor(id = id)
        vendor.is_active = False
        vendor.updated_by = self.request.user.id
        vendor.save()
        return redirect("vendors:vendor-list")
