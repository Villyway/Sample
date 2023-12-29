import json

from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import View
from django.db import transaction
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.core import serializers
from django.template.loader import render_to_string

from .forms import VendorForm
from .models import Vendor, PartyType
from utils.models import Address
from utils.views import decode_data
from .serializers import VendorDetailSerializer



# Product Dashboard
class Dashboard(View):
    template_name = "vendors/dashboard.html"

    def get(self, request):
        return render(request,self.template_name)


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
    
    def post(self,request):
        gst_no = Vendor.objects.filter(gst_no=request.POST.get('gst_no'))
        if gst_no:
            vendor = Vendor.objects.get(gst_no=request.POST.get('gst_no'))
            return redirect("vendors:vendor-edit",vendor.id)
        else:
            messages.error(self.request,"This Vendor is not found, Please add the vendor.")
            return redirect("vendors:vendor-list")

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
                    type =  form_data["type"],
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

                if vendor.type != form_data['type']:
                    vendor.type = form_data["type"]

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


class GetVenderName(View):
    def get(self, request,id):
        vendor = VendorDetailSerializer(Vendor.objects.single_vendor(id = id)).data
        # vendor = serializers.serialize("json",Vendor.objects.single_vendor(id = id))
        data = {
            "vendor": vendor
        }
        return JsonResponse(data)
    

#Category
class CreateCategories(View):
    template_name = "vendors/category.html"
    
    def get(self, request):
        categories = PartyType.objects.filter(is_active=True)
        previous_url = request.META.get('HTTP_REFERER')
        context = {
            "categories": categories,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        try:
            data = json.loads(request.POST.get("data"))
            if data["category"] != '':
                category = data["category"]
                obj, created = PartyType.objects.get_or_create(
                    type__iexact=category,
                    defaults={
                        'type': category
                    },
                    is_active =True,
                    created_by = self.request.user.id
                )
                
            
            categories = PartyType.objects.filter(is_active=True)
            html = render_to_string(
                template_name="components/categories_table.html",
                context={"categories": categories}
            )

            data_dict = {
                "data": html
            }
            return JsonResponse(data=data_dict, safe=False)

        except Exception as e:
            data = {
                "error": str(e),
                "status": 500
            }
            return JsonResponse(data)


class RemoveVendorCategory(View):

    def post(self, request):
        try:
            category_id = request.POST.get("id")
            category_obj = PartyType.objects.get(id=category_id)
            category_obj.is_active = False
            category_obj.save()
            categories = PartyType.objects.filter(is_active=True)
            html = render_to_string(
                template_name="components/categories_table.html",
                context={"categories": categories}
            )
            data_dict = {
                "data": html
            }
            return JsonResponse(data=data_dict, safe=False)

        except Exception as e:
            data = {
                "error": str(e),
                "status": 500
            }
            return JsonResponse(data)
