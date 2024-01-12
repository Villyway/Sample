import json

from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import View
from django.db import transaction
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string

from .forms import VendorForm
from .models import Vendor, PartyType
from utils.models import Address, Country, State, City
from utils.views import decode_data
from .serializers import VendorDetailSerializer
from products.models import Product, VendorWithProductData



# Product Dashboard
class Dashboard(View):
    template_name = "vendors/dashboard.html"

    def get(self, request):
        return render(request,self.template_name)


class VendorList(View):
    template_name = "vendors/list.html"

    def get(self, request):
        vendors = Vendor.objects.active().order_by('-created_at')
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
                    type = form_data['type'],
                    comany_name = form_data['comany_name'],
                    primary_contect_name = form_data['primary_contect_name'],
                    secondary_contect_name = form_data['secondary_contect_name'],
                    mobile = form_data['mobile1'],
                    mobile1 = form_data['mobile2'],
                    email = form_data['email1'],
                    email1 = form_data['mobile2'],
                    gst_no = form_data['gst_no'],
                    created_by = self.request.user.id
                )
                address = Address()
                address.street = form_data["street"]
                address.street2 = form_data["street2"]
                if form_data["country"].name == 'Other':
                    address.country = Country.objects.crate_country(form_data["other_country"])
                else:
                    address.country = form_data["country"]
                
                if form_data["state"].name == 'Other':
                    address.state = State.objects.create_state(form_data["other_state"], address.country)
                else:
                    address.state = form_data["state"]
                
                if form_data["city"].name == 'Other':
                    address.city = City.objects.create_city(form_data["other_city"], address.state)
                else:
                    address.city = form_data["city"]
                
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
    
    def form_invalid(self, form):
        vendor = Vendor.objects.single_vendor(
            id= self.kwargs["id"])
        super(VendorEditView, self).form_invalid(form)
        messages.error(self.request,form.errors)
        return redirect("vendors:vendor-edit",vendor.id)
    
    def form_valid(self, form):
        form_data = form.cleaned_data
        print(form_data)
        # try:
        with transaction.atomic():
            
            vendor = Vendor.objects.single_vendor(id = self.kwargs['id'])
            if vendor.type != form_data['type']:
                vendor.type = form_data['type']
            if vendor.comany_name != form_data['comany_name']:
                vendor.comany_name = form_data['comany_name']
            if vendor.primary_contect_name != form_data['primary_contect_name']:
                vendor.primary_contect_name = form_data['primary_contect_name']
            if vendor.secondary_contect_name != form_data['secondary_contect_name']:
                vendor.secondary_contect_name = form_data['secondary_contect_name']
            if vendor.mobile != form_data['mobile1']:
                vendor.mobile = form_data['mobile1']
            if vendor.mobile1 != form_data['mobile2']:
                vendor.mobile1 = form_data['mobile2']
            if vendor.email != form_data['email1']:
                vendor.email = form_data['email1']
            if vendor.email1 != form_data['mobile2']:
                vendor.email1 = form_data['mobile2']
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
                if form_data["country"].name == 'Other':
                    address.country = Country.objects.crate_country(form_data["other_country"])
                else:
                    address.country = form_data["country"]
            if address.state != form_data["state"]:
                if form_data["state"].name == 'Other':
                    address.state = State.objects.create_state(form_data["other_state"], address.country)
                else:
                    address.state = form_data["state"]
            if address.city != form_data["city"]:
                if form_data["city"].name == 'Other':
                    address.city = City.objects.create_city(form_data["other_city"], address.state)
                else:
                    address.city = form_data["city"]
            if address.zip != form_data["pincode"]:
                address.zip = form_data["pincode"]
            address.updated_by = self.request.user.id
            address.save()
            messages.success(self.request,"Vendor Successfully Updated!!")
            return redirect('vendors:vendor-list')
            
        # except Exception as e:
            # messages.error(self.request, str(e))
            # print(str(e))
            # return redirect(self.request.META['HTTP_REFERER'])


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



class VendorDetails(View):

    template_name = "vendors/show.html"

    def get(self, request, id):
        vendor = Vendor.objects.get(id=id)
        products = vendor.vendorwithproductdata_set.is_active()
        address = vendor.address.first()
        
        context = {
            "vendor":vendor,
            "address":address,
            "products":products

        }
        return render(request,self.template_name,context)
    
    def post(self, request, id):
        vendor = Vendor.objects.get(id=id)
        products = request.POST.getlist('productCode[]')
        price = request.POST.getlist('quantity[]')

        for product_name, price in zip(products, price):
            product = Product.objects.get(part_no = product_name)
            VendorWithProductData.objects.create(vendor=vendor, product=product, price=price)
            
        return redirect("vendors:vendor-details",vendor.id)
    

def DeleteVendorOfProduct(View):

    def get(self, request, id):

        product = VendorWithProductData.objects.get(id=id)
        product.is_active = False
        product.save()
        return redirect("vendors:vendor-details",product.vendor.id)