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
from .models import InWord, Outword, SimpleStockUpdte
from utils.views import get_secured_url, is_ajax
from .serializers import InwordOfBillWiseProductSerializer, StockHistorySerializer
from products.models import Product, Categories
from utils.constants import StockTransection
from utils.constants import ReportTimeLine, InventryReportType
from inventry.resources import StockUpdateReport


# Create your views here.

# Dashboard
class Dashboard(View):
    template_name = "inventry/dashboard.html"

    def get(self, request):
        
        category = Categories.objects.get(name="Finish Goods")
        finished_product = Product.objects.category_wise(category)[:10]

        context = {
            "finished_item": finished_product
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
    success_url = "/inventry/dashboard"

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
            print(form_data)
            with transaction.atomic():
                part = Product.objects.by_part_no(form_data['part_no'])
                stock = SimpleStockUpdte()
                stock.part = part
                stock.old_stock = part.stock
                stock.received_by = form_data['receive_by']
                stock.received_qty = form_data['qty']
                if form_data['transection_type'] == StockTransection.DR.value:
                    if part.stock > int(stock.received_qty):
                        stock.transection_type = StockTransection.DR.value
                        stock.quantity_on_hand = part.stock - int(form_data['qty'])
                    else:
                        messages.error(
                        self.request, part.part_no + "-"+ part.name +" of issued quantity is greater then availabel stock quantity.")
                        data = {
                            'error':part.part_no + "-"+ part.name +" of issued quantity is greater then availabel stock quantity.",
                            "status": 403
                        }
                        return JsonResponse(data)
                        

                else:
                    stock.transection_type = StockTransection.CR.value
                    stock.quantity_on_hand = part.stock + int(form_data['qty'])

                
                stock.save()
                part.stock = stock.quantity_on_hand
                part.save()             
                
            data = {
                        'message': "Product added successfully.",
                        'url': get_secured_url(
                            self.request) + self.request.META["HTTP_HOST"] + 'inventry/add-stock/'
                    }
            return JsonResponse(data, status = 200)


# This is by get stock transection
class StockHistoryInJson(View):
    
    def get(self,request, id):
        try:
            histories = SimpleStockUpdte.objects.single_itme_of_history(Product.objects.by_part_no(id))[:12]
            html = render_to_string(
                template_name="components/stock-trans-his.html",
                context={"histories": histories}
            )
            data_dict = {
                "data": html
            }
            return JsonResponse(data=data_dict, safe=False)
        except Exception as e:
            data = {"error": str(e), "status": 403}
            return JsonResponse(data)


# History of Stock
class StockHistoriesList(View):

    template_name = "inward/histories.html"

    def get(self, request):
         
        products = SimpleStockUpdte.objects.active()
        results_per_page = 15
        page = request.GET.get('page', 1)
        paginator = Paginator(products, results_per_page)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        context = {
            "products": products,
            "data" : [page,results_per_page]

        }
        return render(request, self.template_name, context)


class InventryReport(View):

    template_name = "inventry/report.html"

    def get(self, request):
        # print([(e.name,e.value) for e in ReportTimeLine])
        return render(request, self.template_name)


class InventryReportStock(View):
    template_name = "components/report-stock.html"

    def get(self,request):
        try:           
            if is_ajax(request):
                start_date = request.GET.get("start", None)
                end_date = request.GET.get("end", None)
                category = request.GET.get("category", None)
                export_data = request.GET.get("export", None)

                if category == ReportTimeLine.TODAY.value:
                    products = SimpleStockUpdte.objects.today_report()
                else:
                    products = SimpleStockUpdte.objects.today_report()
                
                if export_data:
                    print("hi")
                    product_resourse = StockUpdateReport()
                    dataset = product_resourse.export(products)
                    response = HttpResponse(dataset.csv,content_type="text/csv")
                    time_name = datetime.now().strftime("%Y%m%d-%H%M%S")
                    response['Content-Disposition'] = 'attachment; filename="stock_report'+ time_name + '".csv"'
                    return response
                else:
                    html = render_to_string(
                        template_name=self.template_name,
                        context={"products": products}
                    )

                    data_dict = {
                        "data": html
                    }
                    return JsonResponse(data=data_dict, safe=False)

            if request.META.get('HTTP_REFERER'):
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                return redirect("products:list")
        except Exception as e:
            return JsonResponse({"error": str(e)})





class ExportData(View):
    
    def get(self, request):
        product_resourse = StockUpdateReport()
        # queryset = SimpleStockUpdte.objects.today_report()
        queryset = SimpleStockUpdte.objects.today_report()
        dataset = product_resourse.export(queryset)
        response = HttpResponse(dataset.csv,content_type="text/csv")
        time_name = datetime.now().strftime("%Y%m%d-%H%M%S")
        response['Content-Disposition'] = 'attachment; filename="stock_report'+ time_name + '".csv"'
        return response
        