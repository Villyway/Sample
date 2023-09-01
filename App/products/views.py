import os
import json

from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import View
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, Http404
from django.template.loader import render_to_string
from django.core.files.storage import default_storage

from .models import Product, Attribute, ProductAttribute, InWord, Outword
from .forms import ProductForm, InWardForm, OutWardForm
from utils.views import get_secured_url

# Product List
class ProductList(View):
    template_name = "products/list.html"

    def get(self,request):
        data = {
            "products" : Product.objects.all(),
        }
        return render(request,self.template_name,context=data)
    

# Product Create.
class CreateProduct(FormView):
    form_class = ProductForm
    template_name = "products/create.html"

    def form_invalid(self, form):
        super(CreateProduct, self).form_invalid(form)
        messages.error(self.request,form.errors)
        return redirect("products:products-create")

    def form_valid(self, form):
        form_data = form.cleaned_data
        try:
            with transaction.atomic():
                product = Product()
                product.code = form_data['code']
                product.description = form_data['description']
                product.umo = form_data['umo']
                product.specification = form_data['specification']
                product.stock = form_data['stock']
                product.minimum_stock_level  = form_data['minimum_stock_level']
                product.rack_no = form_data['rack_no']
                product.tray_no = form_data['tray_no']
                product.created_by = self.request.user.id
                product.save()
                if form_data['image']:
                    product.save_image_url(form_data["image"], get_secured_url(
                            self.request) + self.request.META["HTTP_HOST"])
            return redirect(get_secured_url(
                            self.request) + self.request.META["HTTP_HOST"] + '/products/' + str(product.id) + '/product-property/')
        
        except Exception as e:
            messages.error(self.request, str(e))
            return redirect("products:products-create")


#Product Edit
class ProductEditView(FormView):
    form_class = ProductForm
    template_name = "products/edit.html"

    def get_form_kwargs(self):
        product = Product.objects.single_product(
            id= self.kwargs["id"])
        kwargs = super(ProductEditView, self).get_form_kwargs()
        kwargs.update({"product": product, "edit": True})
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(ProductEditView, self).get_context_data(**kwargs)
        product = Product.objects.single_product(id=self.kwargs["id"])
        context['product'] = product
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        return context
    
    def form_invalid(self, form):
        super(ProductEditView, self).form_invalid(form)
        print(form.errors)
        messages.error(self.request,form.errors)
        return redirect(self.request.META['HTTP_REFERER'])
    
    def form_valid(self, form):
        form_data = form.cleaned_data
        try:
            with transaction.atomic():
                product = Product.objects.single_product(id = self.kwargs['id'])
                if product.code != form_data['code']:
                    product.code = form_data['code']
                if product.description != form_data['description']:
                    product.description = form_data['description']
                if product.umo != form_data['umo']:
                    product.umo = form_data['umo']
                if product.specification != form_data['specification']:
                    product.specification = form_data['specification']
                if product.stock != form_data['stock']:
                    product.stock = form_data['stock']
                if product.minimum_stock_level != form_data['minimum_stock_level']:
                    product.minimum_stock_level = form_data['minimum_stock_level']
                if product.rack_no != form_data['rack_no']:
                    product.rack_no = form_data['rack_no']
                if product.tray_no != form_data['tray_no']:
                    product.tray_no = form_data['tray_no']
                product.updated_by = self.request.user.id
                product.save()
                if form_data['image']:
                    old_image = '/'.join(product.image.split('/')[4:])
                    if default_storage.exists(old_image):
                        default_storage.delete(old_image)

                    product.save_image_url(form_data["image"], get_secured_url(
                            self.request) + self.request.META["HTTP_HOST"])
                return redirect('products:products-list')
            
        except Exception as e:
            messages.error(self.request, str(e))
            return redirect(self.request.META['HTTP_REFERER'])


class ProductProperty(View):
    template_name = "products/attribute.html"

    def get(self, request, id):
        product = Product.objects.single_product(id)
        properties = ProductAttribute.objects.filter(product=product)
        attribute = Attribute.objects.all()
        previous_url = request.META.get('HTTP_REFERER')
        context = {
            "product": product,
            "properties": properties,
            "previous_url": previous_url,
            "attribute": attribute
        }

        return render(request, self.template_name, context)
    # template_name = "products/attribute.html"components/attributes_table.html

    # def get(self, request, id):
    #     product = Product.objects.single_product(id)
    #     properties = ProductAttribute.objects.filter(product=product)
    #     attribute = Attribute.objects.all()
    #     if "products/create/" in request.META.get('HTTP_REFERER'):
    #         previous_url = get_secured_url(
    #             self.request) + self.request.META["HTTP_HOST"] + '/products/list/'
    #     else:
    #         previous_url = request.META.get('HTTP_REFERER')

    #     context = {
    #         "product": product,
    #         "properties": properties,
    #         "previous_url": previous_url,
    #         "attribute": attribute
    #     }
    #     return render(request, self.template_name, context)
    

    def post(self, request, id):
        product = Product.objects.single_product(id)
        try:
            data = json.loads(request.POST.get("data"))
            if data["attribute"] != '' and data["value"] != '':
                attribute = data["attribute"]
                value = data["value"].strip()
                obj, created = Attribute.objects.get_or_create(
                    name__iexact=attribute,
                    defaults={
                        'name': attribute
                    }
                )
                check_same_property = ProductAttribute.objects.match_same_attribute(
                    product=product, attribute=obj)
                if not check_same_property:
                    property_obj = ProductAttribute()
                    property_obj.product = product
                    property_obj.attribute = obj
                    property_obj.value = value
                    property_obj.save()
                    error = None
                else:
                    error = "This property was already add."
            else:
                error = "All fields are required."

            properties = ProductAttribute.objects.filter(product=product)
            html = render_to_string(
                template_name="components/attributes_table.html",
                context={"properties": properties, "error": error}
            )

            data_dict = {
                "data": html
            }
            return JsonResponse(data=data_dict, safe=False)

        except Exception as e:
            print(str(e))
            data = {
                "error": str(e),
                "status": 500
            }
            return JsonResponse(data)


class RemoveProductProperty(View):

    def post(self, request):
        try:
            property_id = request.POST.get("id")
            property_obj = ProductAttribute.objects.get(id=property_id)
            product = property_obj.product
            properties = ProductAttribute.objects.filter(product=product)
            property_obj.delete()
            html = render_to_string(
                template_name="components/attributes_table.html",
                context={"properties": properties}
            )
            data_dict = {
                "data": html
            }
            return JsonResponse(data=data_dict, safe=False)

        except Exception as e:
            print(str(e))
            data = {
                "error": str(e),
                "status": 500
            }
            return JsonResponse(data)
        

# inward
class InwardCreateView(FormView):
    form_class = InWardForm
    template_name = "inward/create.html"

    def form_invalid(self, form):
        return super(InwardCreateView).form_invalid(form)
    
    def form_valid(self, form):
        form_data = form.cleaned_data

        try:
            inword = InWord()
            inword.grn_no = form_data['grn_no']
            inword.bill_no = form_data['bill_no']
            inword.bill_date = form_data['bill_date']
            inword.part = form_data['part']
            inword.received_qty = form_data['received_qty']
            inword.uom = form_data['uom']
            inword.in_time = form_data['in_time']
            inword.qc_status = form_data['qc_status']
            inword.purchase_order_no = form_data['purchase_order_no']
            inword.vendor = form_data['vendor']
            inword.receive_by = form_data['receive_by']
            inword.remarks = form_data['remarks']
            inword.created_by = self.request.user.id
            inword.old_stock = form_data['part'].stock
            inword.save()
            if form_data['file_url']:
                inword.save_image_url(form_data["file_url"], get_secured_url(
                                self.request) + self.request.META["HTTP_HOST"])

            # add stock
            product = inword.part
            product.stock = product.stock + int(inword.received_qty  )
            product.save()
            return redirect("products:products-list")
        
        except Exception as e:
            messages.error(self.request, str(e))
            return redirect(self.request.META['HTTP_REFERER'])
    
    

# Outward
class OutwardCreateView(FormView):
    form_class = OutWardForm
    template_name = "outward/create.html"

    def form_invalid(self, form):
        return super(OutwardCreateView).form_invalid(form)
    
    def form_valid(self, form):
        form_data = form.cleaned_data
        out_ward = Outword()
        out_ward.parts = form_data["parts"]
        out_ward.issued_qty = form_data["issued_qty"]
        out_ward.uom = form_data["uom"]
        out_ward.issued_by = self.request.user
        out_ward.received_by = form_data["receive_by"]
        out_ward.remarks = form_data["remarks"]
        out_ward.old_stock = form_data["parts"].stock
        out_ward.save()
        out_ward.generate_out_ward_sr_no()

        # deduct Operations
        product = out_ward.parts
        product.stock = product.stock - int(out_ward.issued_qty)
        product.save()
        return redirect("products:products-list")