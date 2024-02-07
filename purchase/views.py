from wkhtmltopdf.views import PDFTemplateResponse
import json
import csv
from collections import defaultdict

from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.db import transaction

from products.models import Product, BOMItem, VendorWithProductData, Categories
from purchase.models import PurchaseOrder, PaymentTerms, PurchaseItem, TaxCode, TermsAndConditions
from orders.models import OrderOfProduct
from vendors.models import Vendor
from users.models import User
from utils.models import State

from utils.views import is_ajax, get_secured_url


# Create your views here.
class Dashboard(View):

    template_name = "purchase/dashboard.html"

    def get(self, request):
        products_below_minimum_stock = Product.objects.filter(stock__lt=F('minimum_stock_level'))
        context = {
            "products":products_below_minimum_stock,
        }
        return render(request, self.template_name, context)


class MRP(View):
    
    template_name = "purchase/mrp.html"

    def calculate_mrp(self, product, quantity, mrp_dict=None):
        if mrp_dict is None:
            mrp_dict = defaultdict(int)

        bom_items = BOMItem.objects.filter(product=product)

        for bom_item in bom_items:
            raw_material = bom_item.component
            component_quantity = bom_item.quantity * quantity

            # Aggregate the quantity for the same raw material
            mrp_dict[raw_material] += component_quantity

            # Recursively calculate MRP for the raw material
            self.calculate_mrp(raw_material, component_quantity, mrp_dict)
        return mrp_dict

    def aggregate_mrp(self, mrp_results):

        # print()
        aggregated_mrp = defaultdict(int)

        for mrp_result in mrp_results:
            for product, quantity in mrp_result.items():
                aggregated_mrp[product] += quantity

        return aggregated_mrp
    
    def get(self,request):
        return render(request,self.template_name)
    
    def post(self,request):

        # if is_ajax(request):
        product_objs = []
        products = request.POST.getlist('productCode[]')
        quantities = request.POST.getlist('quantity[]')
        for product_name, quantity_value in zip(products, quantities):
            product_objs.append(self.calculate_mrp(Product.objects.by_code(product_name),int(quantity_value)))
        
        results = self.aggregate_mrp(product_objs)
        
        requirements = []
        for i, j in dict(results).items():
            __p = {}
            __p['id'] = i.id
            __p['name'] = i.part_no+" - "+i.name
            __p['qty'] = j
            if i.stock - j < 0:
                __p['available_stock'] = 0
            elif i.stock - j > 0:
                __p['available_stock'] = i.stock - j
            __p['current_stock'] = i.stock
            if i.stock - j > 0:
                __p['requirement'] = 0
            elif i.stock - j < 0:
                __p['requirement'] = i.stock - j
            requirements.append(__p)
        
        # Export as CSV if requested
        # if request.POST.get('export_csv'):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="requirements.csv"'
        csv_writer = csv.writer(response)
        # Write CSV header
        csv_writer.writerow(['ID', 'Name', 'Quantity', 'Current Stock', 'Requirement', 'Available Stock'])
        for requirement in requirements:
            csv_writer.writerow([
                requirement['id'],
                requirement['name'],
                requirement['qty'],
                requirement['current_stock'],
                requirement['requirement'],
                requirement['available_stock']
            ])
        return response

            # data_dict = {
                # "data":json.dumps(requirements, indent = 4), 
            # }
            # return JsonResponse(data=data_dict, safe=False)            
            

# PO
class CreatePurchaseOrder(View):
    template_name = "purchase/create.html"

    def get(self, request, product=None):
        vendors = None
        
        if PurchaseOrder.objects.last():
            po_no = int(PurchaseOrder.objects.first().po_no) + 1
            
        else:
            po_no = 1

        if product:
            product = Product.objects.by_part_no(product)
            vendors = product.vendorwithproductdata_set.all()
        else:
            product = None
        context = {
            "product": product,
            "po_no":po_no,
            "vendors":vendors,
            "payment_term":PaymentTerms.objects.all(),
            "product_url" : get_secured_url(
                            self.request) + self.request.META["HTTP_HOST"] + '/vendors/',
            "categories":Categories.objects.all()
        }
        return render(request,self.template_name, context)
    
    def post(self, request, product=None):
        if is_ajax(request):
            po_no = request.POST.get('po_no')
            indent = request.POST.get('indent')
            if indent !='':
                indent = PurchaseOrder.objects.get(po_no=indent)
            else:
                indent = None
            
            product_qty = [item for item in request.POST.getlist('quantity[]') if item != '']
            del_date = [item for item in request.POST.getlist('del_date[]') if item != '']
            product_of_price_obj = request.POST.getlist('selected[]')
            vendor = Vendor.objects.get(id=request.POST.get('vendor'))
            pay_term = request.POST.get('payment_term')
            remark = request.POST.get('remark')

            default_state = State.objects.get(code="GJ")
            tax = []
            if vendor.address.first().state == default_state:
                 tax.append(TaxCode.objects.get(code="CGST"))
                 tax.append(TaxCode.objects.get(code="SGST"))
            else:
                tax.append(TaxCode.objects.get(code="IGST"))
            
            with transaction.atomic():
                po_obj = PurchaseOrder()
                if indent:
                    po_obj.parent = indent
                po_obj.po_no = po_no
                po_obj.vendor = vendor
                po_obj.payment_term = PaymentTerms.objects.get(id = pay_term)
                po_obj.created_by = request.user.id
                po_obj.remarks = remark
                
                po_obj.gl_name = Categories.objects.get(id=request.POST.get('gl_name'))
                po_obj.save()

                for qty, product_obj, del__date in zip(product_qty, product_of_price_obj, del_date):
                    po_item = PurchaseItem()
                    po_item.po = po_obj
                    po_item.part = VendorWithProductData.objects.get(id=product_obj).product
                    po_item.qty = qty
                    po_item.del_date = del__date
                    po_item.price = VendorWithProductData.objects.get(id=product_obj).price
                    po_item.created_by = request.user.id
                    po_item.save()
                
                for i in tax:
                    po_obj.tax_code.add(i)

                for i in TermsAndConditions.objects.all():
                    po_obj.general_terms.add(i)
                
                po_obj.created_by = request.user.id
                po_obj.save()
                PurchaseOrder.objects.calculate_and_save_total(po_obj.id)
                PurchaseOrder.objects.calculate_tax_and_save(po_obj.id)

            return JsonResponse({"error":"Hi"})

        return render(request,self.template_name)
    

class OrderAgainstMRP(View):

    def calculate_mrp(self, product, quantity, mrp_dict=None):
        if mrp_dict is None:
            mrp_dict = defaultdict(int)

        bom_items = BOMItem.objects.filter(product=product)

        for bom_item in bom_items:
            raw_material = bom_item.component
            component_quantity = bom_item.quantity * quantity

            # Aggregate the quantity for the same raw material
            mrp_dict[raw_material] += component_quantity

            # Recursively calculate MRP for the raw material
            self.calculate_mrp(raw_material, component_quantity, mrp_dict)
        return mrp_dict

    def aggregate_mrp(self, mrp_results):

        # print()
        aggregated_mrp = defaultdict(int)

        for mrp_result in mrp_results:
            for product, quantity in mrp_result.items():
                aggregated_mrp[product] += quantity

        return aggregated_mrp

    def post(self, request):
        product_objs = []
        
        order_nos = request.POST.getlist('so[]')
        print(order_nos)

        for i in order_nos:

            for order_item in OrderOfProduct.objects.get_so_no_by_product(i):
                product_objs.append(self.calculate_mrp(order_item.product,int(order_item.order_qty)))

        results = self.aggregate_mrp(product_objs)
                
        requirements = []
        for i, j in dict(results).items():
            __p = {}
            __p['id'] = i.id
            __p['name'] = i.part_no+" - "+i.name
            __p['qty'] = j
            if i.stock - j < 0:
                __p['available_stock'] = 0
            elif i.stock - j > 0:
                __p['available_stock'] = i.stock - j
            __p['current_stock'] = i.stock
            if i.stock - j > 0:
                __p['requirement'] = 0
            elif i.stock - j < 0:
                __p['requirement'] = i.stock - j
            requirements.append(__p)
        
        # Export as CSV if requested
        # if request.POST.get('export_csv'):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="requirements.csv"'
        csv_writer = csv.writer(response)
        # Write CSV header
        csv_writer.writerow(['ID', 'Name', 'Quantity', 'Current Stock', 'Requirement', 'Available Stock'])
        for requirement in requirements:
            csv_writer.writerow([
                requirement['id'],
                requirement['name'],
                requirement['qty'],
                requirement['current_stock'],
                requirement['requirement'],
                requirement['available_stock']
            ])
        return response      


class PoList(View):
    template_name = "purchase/list.html"

    def get(self, request):
        
        purchase_orders = PurchaseOrder.objects.all().order_by('-created_at')
        
        
        context = {
            "pos": purchase_orders,
        }
        return render(request,self.template_name, context)
    
class SingelPurchaseOrder(View):

    template_name = "purchase/show.html"
    def get(self,request,id):
        po = PurchaseOrder.objects.get(id=id)
        context = {
            "po": po,
            "po_address" : po.vendor.address.first(),
            "genrated_by":User.objects.get(id=po.created_by).name
        }
        return render(request,self.template_name, context)
    
    def post(self, request, id):
        po = PurchaseOrder.objects.get(id=id)
        remark = request.POST.get('remark')
        if po.remarks != remark:
            po.remarks = remark
            po.save()
        product_qty = [item for item in request.POST.getlist('quantity[]') if item != '']
        del_date = [item for item in request.POST.getlist('del_date[]') if item != '']
        product_of_price_obj = request.POST.getlist('selected[]')
        
        with transaction.atomic():
            for qty, product_obj, del__date in zip(product_qty, product_of_price_obj, del_date):
                product = VendorWithProductData.objects.get(id=product_obj).product
                if PurchaseItem.objects.filter(part=product, po=po).exists():
                    print(PurchaseItem.objects.filter(part=product, po=po))
                    item = po.purchaseitem_set.get(part=product)
                    if item.qty != qty:
                       item.qty = qty
                    if item.del_date != del__date:
                        item.del_date = del__date                    
                    item.save()
                else:
                    po_item = PurchaseItem()
                    po_item.po = po
                    po_item.part = VendorWithProductData.objects.get(id=product_obj).product
                    po_item.qty = qty
                    po_item.del_date = del__date
                    po_item.price = VendorWithProductData.objects.get(id=product_obj).price
                    po_item.created_by = request.user.id
                    po_item.save()
            PurchaseOrder.objects.calculate_and_save_total(id)
            PurchaseOrder.objects.calculate_tax_and_save(id)

        return redirect(request.path)
    

class ExportPO(View):

    template_name = "purchase/po-export.html"

    def get(self, request, id):
        # You can pass context data if needed
        po = PurchaseOrder.objects.get(id=id)        
        context_data = {
            "po": po,
            "po_address" : po.vendor.address.first(),
            "title" : "PURCHASE ORDER",
            "genrated_by":User.objects.get(id=po.created_by).name
                        }

        # Render the template as PDF
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            filename='output.pdf',
            context=context_data,
            show_content_in_browser=False,
            cmd_options={'margin-top': 10, 'orientation': 'Landscape', 'enable-local-file-access': True},# Optional: Set additional wkhtmltopdf options
        )

        return response


class DeletePoProduct(View):

    def get(self,request,id):
        product = PurchaseItem.objects.get(id=id)
        if product.po.status:
            with transaction.atomic():
                po_id = product.po.id
                product.delete()

                PurchaseOrder.objects.calculate_and_save_total(po_id)
                PurchaseOrder.objects.calculate_tax_and_save(po_id)
                messages.success(
                                request, "Purchase Order of product.product.part_no successfully remove from purchase order.")
        else:
            messages.error(request, "THIS PO WAS ALREADY CLOSED THEN NO CHANGES AVAILABEL!")
        
        return redirect('purchase:purchase-singel-order',id=product.po.id)
    




        


