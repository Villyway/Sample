import os
import json

from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import View
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, Http404

from .forms import InWardForm, OutWardForm
from .models import InWord, Outword
from utils.views import get_secured_url

# Create your views here.

# inward
class InwardCreateView(FormView):
    form_class = InWardForm
    template_name = "inward/create.html"

    def form_invalid(self, form):
        super(InwardCreateView, self).form_invalid(form)
        messages.error(self.request,form.errors)
        return redirect("products:inward")
    
    
    def form_valid(self, form):
        form_data = form.cleaned_data

        # try:
        inword = InWord()
        inword.grn_no = form_data['grn_no']
        inword.bill_no = form_data['bill_no']
        inword.bill_date = form_data['bill_date']
        inword.part = form_data['part']
        inword.received_qty = form_data['received_qty']
        inword.uom = form_data['part'].umo
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
        if inword.qc_status:
            product = inword.part
            product.stock = product.stock + int(inword.received_qty)
            product.save()
        return redirect("products:products-list")
        
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