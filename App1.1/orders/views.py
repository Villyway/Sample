from django.shortcuts import render, redirect

# Create your views here.
from datetime import datetime

from django.views.generic import View
from django.contrib import messages
from django.db import transaction
from django.views.generic.edit import FormView
from django.http import HttpResponse, JsonResponse, Http404

from orders.forms import OrdersForm
from utils.views import get_secured_url, is_ajax, generate_order_dispatch_no
from customers.models import Customer
from products.models import Product
from orders.models import OrderDetails, OrderOfProduct
from utils.constants import PackingType, OrderUOM, OrderStatus, DispatchStatus
from utils.models import Address


class Dashboard(View):
    template_name = "orders/dashboard.html"

    def get(self,request):

        return render(request,self.template_name)
    

class CreateOrders(View):
    template_name = "orders/create.html"
    success_url = "/orders/dashboard/"

    def get(self,request, id):
        if Customer.objects.filter(id=id).exists():
            customer = Customer.objects.get(id=id)
        products = Product.objects.finished_product()
        context = {
            'products': products,
            'customer': customer,
            'unit' :[e.value for e in OrderUOM], 
            'packaging_type' : [e.value for e in PackingType]

        }
        return render(request,self.template_name, context)
    
    def post(self, request, id):
        if is_ajax(self.request):
            with transaction.atomic():
                products = request.POST.getlist('productCode[]')
                quantities = request.POST.getlist('quantity[]')
                units = request.POST.getlist('unit[]')
                packaging_types = request.POST.getlist('packagingType[]')
                bill_add = request.POST.get('billingto')
                ship_add = request.POST.get('shippedto')

                if Customer.objects.filter(id=id).exists():
                    customer_obj = Customer.objects.get(id = id)

                    order = OrderDetails()
                    order.customer = customer_obj
                    order.date = datetime.today().date()
                    order.remarks = request.POST.get('remark')
                    order.created_by = request.user.id
                    order.billing_add = Address.objects.get(id=bill_add)
                    order.shipped_add = Address.objects.get(id=ship_add)
                    order.save()
                    order.order_no = generate_order_dispatch_no(order.id)
                    order.save()

                    for product_name, quantity_value, p_unit, p_type in zip(products, quantities, units, packaging_types):
                        if Product.objects.by_code(product_name):
                            product = Product.objects.by_code(product_name)
                            order_of_product = OrderOfProduct()
                            order_of_product.order = order
                            order_of_product.product = product
                            order_of_product.order_qty = quantity_value
                            order_of_product.uom = p_unit
                            order_of_product.packing_type = p_type
                            order_of_product.created_by = request.user.id
                            order_of_product.save()
                messages.success(
                    self.request, "Order added successfully.")
            data = {
                    'message': "Order added successfully.",
                    'url': get_secured_url(
                        self.request) + self.request.META["HTTP_HOST"] + 'orders/orders-list'
                }
            return JsonResponse(data)
        else:
            return redirect("orders:orders-create")


# Order list
class OrderList(View):
    template_name = "orders/list.html"

    def get(self,request):

        orders = OrderDetails.objects.all()
        context = {"orders":orders}
        return render(request,self.template_name, context)


#singel Order Process
class SingelOrderView(View):

    template_name = "orders/show.html"

    def get(self, request, id):

        order_details =  OrderDetails.objects.get(id=id)
        context = {
            "order" : order_details,
            "dispatch_status": [i.value for i in DispatchStatus],
            "order_status":[i.value for i in OrderStatus],
        }
        return render(request, self.template_name, context)
        

class ChangeDispatchStatusOfOrderOfChild(View):

    def get(self,request, id):
        print(request.GET.get("status", None))
        status = request.GET.get("status", None)
        obj = OrderOfProduct.objects.get(id=id)
        obj.dispatch_status = status
        if DispatchStatus.DISPATCHED.value == status:
            obj.dispatch_date = datetime.now()
        obj.save()

        # Main Order sheet Changes
        all_order = OrderOfProduct.objects.filter(order=obj.order).count()
        dispatch_total = OrderOfProduct.objects.filter(order=obj.order, dispatch_status=DispatchStatus.DISPATCHED.value).count()
        if all_order == dispatch_total:
            main_order = OrderDetails.objects.get(id = obj.order.id)
            main_order.dispatch_status = DispatchStatus.DISPATCHED.value
            main_order.dispatch_date = datetime.now()
            main_order.save()
        
        data = {
                    'message': "",
                    'url': get_secured_url(
                        self.request) + self.request.META["HTTP_HOST"] + 'orders/'+ str(obj.order.id) +'/order-details'
                }
        return redirect("orders:order-details",id=obj.order.id)
    

# Change Delevar status

class ChangeDeliveryStatus(View):

    def get(self, request, id):
        status = request.GET.get("status", None)
        obj = OrderOfProduct.objects.get(id=id)
        obj.status = status
        if OrderStatus.DELIVERED.value == status:
            obj.delivered_date = datetime.today()
        obj.save()

        # Main Order sheet Changes
        all_order = OrderOfProduct.objects.filter(order=obj.order).count()
        dispatch_total = OrderOfProduct.objects.filter(order=obj.order, status=OrderStatus.DELIVERED.value).count()
        if all_order == dispatch_total:
            main_order = OrderDetails.objects.get(id = obj.order.id)
            main_order.order_status = OrderStatus.DELIVERED.value
            main_order.pickup_by_party_date = datetime.now()
            main_order.save()
        
        data = {
                    'message': "",
                    'url': get_secured_url(
                        self.request) + self.request.META["HTTP_HOST"] + 'orders/'+ str(obj.order.id) +'/order-details'
                }
        return redirect("orders:order-details",id=obj.order.id)


class OrderDispatchProcess(View):
    template_name = "orders/dispatch_process.html"

    def get(self, request, id):

        order = OrderDetails.objects.get(id=id)
        products = OrderOfProduct.objects.filter(dispatch_status=DispatchStatus.READY.value)
        


        context = {
            "order_details" : order,
            "products" : products,
        }
        return render(request, self.template_name, context)
    
    def post(self,request, id):
        obj = OrderOfProduct.objects.get(id=id)

        print(request.POST)

        return redirect("orders:order-details",id=obj.order.id)


# class CreateOrders1(FormView):
    
#     template_name = "orders/create.html"
#     form_class = OrdersForm
#     success_url = "/orders/dashboard/"

#     def form_invalid(self, form):
#         response = super(CreateOrders, self).form_invalid(form)
#         if is_ajax(self.request):
#             data = form.errors
#             return JsonResponse(data, status=400)
#         else:
#             return redirect('/redirect-success/')

#     def form_valid(self, form):
#         response = super(CreateOrders, self).form_valid(form)
#         try:
#             if is_ajax(self.request):
#                 form_data = form.cleaned_data
#                 with transaction.atomic():
#                     products = self.request.POST.getlist('product[]')
#                     quantities = self.request.POST.getlist('quantity[]')

#                     for product_name, quantity_value in zip(products, quantities):
#                         print(product_name, quantity_value)

                    
#                     messages.success(
#                         self.request, "Product added successfully.")
#                 data = {
#                         'message': "Product added successfully.",
#                         'url': get_secured_url(
#                             self.request) + self.request.META["HTTP_HOST"] + '/products/' + str(1) + '/product-property/'
#                     }
#                 return JsonResponse(data)
#             else:
#                 return response
        
#         except Exception as e:
#             data = {"error": str(e), "status": 403}
#             return JsonResponse(data)


