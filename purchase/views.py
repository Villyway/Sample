import json
import csv
from collections import defaultdict

from django.db.models import F
from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string

from products.models import Product, BOMItem
from purchase.models import PurchaseOrder

from utils.views import is_ajax



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
        if PurchaseOrder.objects.last():
            po_no = int(PurchaseOrder.Objects.last().po_no) + 1
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
            "vendors":vendors
        }
        return render(request,self.template_name, context)