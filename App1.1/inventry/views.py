import os
import json
from datetime import datetime

from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import View
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, Http404
from django.core import serializers
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import InWardForm, OutWardForm, StockForm
from .models import InWord, Outword
from utils.views import get_secured_url, is_ajax
from .serializers import InwordOfBillWiseProductSerializer
from products.models import Product


# Create your views here.

# Dashboard
class Dashboard(View):
    template_name = "inventry/dashboard.html"

    def get(self, request):
        total_products = Product.objects.filter(is_active=True).count()
        context = {
            "total_product":total_products
        }
        return render(request,self.template_name, context)



# inward
class InwardCreateView(FormView):
    form_class = InWardForm
    template_name = "inward/create.html"
    success_url = "/products/list/"

    def form_invalid(self, form):
        response = super(InwardCreateView, self).form_invalid(form)
        if is_ajax(self.request):
            data = form.errors
            return JsonResponse(data, status=400)
        else:
            return response
    
    
    def form_valid(self, form):
        response = super(InwardCreateView, self).form_valid(form)     
        if is_ajax(self.request):
            form_data = form.cleaned_data
        # try:
            with transaction.atomic():
                inword = InWord()
                inword.grn_no = form_data['grn_no']
                inword.bill_no = form_data['bill_no']
                inword.bill_date = form_data['bill_date']
                inword.part = form_data['part']
                inword.received_qty = form_data['received_qty']
                inword.uom = form_data['part'].umo
                inword.in_time = datetime.now()
                inword.qc_status = False
                inword.purchase_order_no = form_data['purchase_order_no']
                inword.vendor = form_data['vendor']
                inword.receive_by = self.request.user
                inword.remarks = form_data['remarks']
                inword.created_by = self.request.user.id
                inword.old_stock = form_data['part'].stock
                inword.save()
                if form_data['file_url']:
                    inword.save_image_url(form_data["file_url"], get_secured_url(
                                    self.request) + self.request.META["HTTP_HOST"])
                # add stock
                if inword.qc_status:
                    product = inword.part
                    product.stock = product.stock + int(inword.received_qty)
                    product.save()
                messages.success(
                        self.request, "Inword added successfully.")
                inwords = InwordOfBillWiseProductSerializer(InWord.objects.filter(bill_no=inword.bill_no)).data
            
            data_dict = {
                "data": inwords
            }
            return JsonResponse(data=data_dict, safe=False)
        else:
            return response
        
        # except Exception as e:
            # messages.error(self.request, str(e))
            # return redirect(self.request.META['HTTP_REFERER'])
    
    

# Outward
class OutwardCreateView(FormView):
    form_class = OutWardForm
    template_name = "outward/create.html"

    def form_invalid(self, form):
        super(OutwardCreateView, self).form_invalid(form)
        messages.error(self.request,form.errors)
        return redirect("products:outword")
    
    def form_valid(self, form):
        form_data = form.cleaned_data
        out_ward = Outword()
        out_ward.parts = form_data["parts"]
        out_ward.issued_qty = form_data["issued_qty"]
        out_ward.uom = form_data["parts"].umo
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
    

#Bill no wise inword data
class GetBillNoByInword(View):

    def get(self, request,id):
        inwords = InwordOfBillWiseProductSerializer(InWord.objects.filter(bill_no=id)).data
        # vendor = serializers.serialize("json",Vendor.objects.single_vendor(id = id))
        # html = render_to_string(
        #         template_name="inward/inword_create_component.html",
        #         context={"inwords": inwords}
        # )
        data_dict = {
            "data": inwords
        }
        return JsonResponse(data=data_dict, safe=False)
    

#QC Process 
class QCView(View):
    template_name = "inward/qc_list.html"

    def get(self, request):
        list_qc = InWord.objects.qc_list()

        page = request.GET.get('page',1)
        paginator = Paginator(list_qc,10)
        try:
            list_qc = paginator.page(page)
        except PageNotAnInteger:
            list_qc = page.page(1)
        except EmptyPage:
            list_qc = paginator.page(paginator.num_pages)
        
        context = {
            "qc_list" : list_qc,
        }
        return render(request,self.template_name, context)
    
    def post(self, request):
        return redirect("inventry:qc-list")
    
    
# Simple Add Stock
class SimpleAddStock(FormView):

    template_name = "inward/add_stock.html"
    form_class = StockForm
    success_url = ""

    def form_invalid(self, form):
        response = super(SimpleAddStock, self).form_invalid(form)
        if is_ajax(self.request):
            data = form.errors
            return JsonResponse(data, status=400)
        else:
            return response
        
    def form_valid(self, form):
        response = super(SimpleAddStock, self).form_valid(form)     
        if is_ajax(self.request):
            form_data = form.cleaned_data
            return redirect("inventry:inventry-dashboard")
