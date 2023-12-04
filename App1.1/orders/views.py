from django.shortcuts import render, redirect

# Create your views here.
from datetime import datetime

from django.views.generic import View
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse

from utils.views import get_secured_url, is_ajax, generate_order_dispatch_no
from customers.models import Customer
from products.models import Product
from orders.models import OrderDetails, OrderOfProduct
from utils.constants import PackingType, OrderUOM, OrderStatus, DispatchStatus, OrderConfirmation, Roles
from utils.models import Address

from wkhtmltopdf.views import PDFTemplateResponse

class Dashboard(View):
    template_name = "orders/dashboard.html"

    def get(self,request):
        total_order = OrderDetails.objects.orders(count=True)
        totla_orders_list = OrderDetails.objects.orders()[:10]
        total_hold_orders = OrderDetails.objects.orders_filtered_by_confirmation(OrderConfirmation.HOLD.value, count=True)
        total_hold_orders_list = OrderDetails.objects.orders_filtered_by_confirmation(OrderConfirmation.HOLD.value)[:10]
        total_confirmed_orders = OrderDetails.objects.orders_filtered_by_confirmation(OrderConfirmation.CONFIRMED.value, count=True)
        total_confirmed_orders_list = OrderDetails.objects.orders_filtered_by_confirmation(OrderConfirmation.CONFIRMED.value)[:10]
        total_in_review_orders = OrderDetails.objects.orders_filtered_by_confirmation(OrderConfirmation.IN_REVIEW.value, count=True)
        total_in_review_orders_list = OrderDetails.objects.orders_filtered_by_confirmation(OrderConfirmation.IN_REVIEW.value)[:10]

        #Order of products.       
        context = {
            "total_orders":total_order,
            "totla_orders_list" : totla_orders_list,
            "total_hold_orders" : total_hold_orders,
            "total_hold_orders_list":total_hold_orders_list,
            "total_confirmed_orders":total_confirmed_orders,
            "total_confirmed_orders_list":total_confirmed_orders_list,
            "total_in_review_orders" : total_in_review_orders,
            "total_in_review_orders_list":total_in_review_orders_list,
            
        }
        return render(request,self.template_name,context)
    
    

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
                        self.request) + self.request.META["HTTP_HOST"] + '/orders/orders-list'
                }
            return JsonResponse(data)
        else:
            return redirect("orders:orders-create")


# Order list
class OrderList(View):
    template_name = "orders/list.html"

    def get(self,request):
        in_review_orders = OrderDetails.objects.orders_filtered_by_confirmation(OrderConfirmation.IN_REVIEW.value)
        # Holding_orders = OrderDetails.objects.orders_in_hold()
        orders = OrderDetails.objects.orders()
        context = {"orders":orders,"confirm_status": [i.value for i in OrderConfirmation],}
        return render(request,self.template_name, context)
    
    def post(self,request):
        if is_ajax(request):
            order_no = request.POST.get('order_no')
            status = request.POST.get('status')
            reason = request.POST.get('reason')
            order =OrderDetails.objects.singel_order_by_order_no(order_no)
            if order:
                order.order_confirmation = status
                order.order_confirmation_remark = reason
                order.updated_by = request.user.id
                order.save()
            
        data = {
                    'message': order_no + "was in" + order.order_confirmation,
                    'url': get_secured_url(
                        self.request) + self.request.META["HTTP_HOST"] + '/orders/orders-list'
                }
        return JsonResponse(data)
    


#singel Order Process
class SingelOrderView(View):

    template_name = "orders/show.html"

    def get(self, request, id):

        order_details =  OrderDetails.objects.get(id=id)
        if order_details.orderofproduct_set.filter(dispatch_status=DispatchStatus.READY.value).count() == 0:
            dn = 0
        else:
            dn=1
        context = {
            "order" : order_details,
            "dispatch_status": [i.value for i in DispatchStatus],
            "order_status":[i.value for i in OrderStatus],
            'unit' :[e.value for e in OrderUOM], 
            'packaging_type' : [e.value for e in PackingType],
            'dn' : dn
        }
        return render(request, self.template_name, context)
    
    def post(self, request, id):
        if is_ajax(self.request):
            order =  OrderDetails.objects.get(id=id)
            products = request.POST.getlist('productCode[]')
            quantities = request.POST.getlist('quantity[]')
            units = request.POST.getlist('unit[]')
            packaging_types = request.POST.getlist('packagingType[]')
            bill_add = request.POST.get('billingto')
            ship_add = request.POST.get('shippedto')

            if order.remarks != request.POST.get('remark'):
                order.remarks = request.POST.get('remark')

            if order.shipped_add != Address.objects.get(id=ship_add):
                order.shipped_add = Address.objects.get(id=ship_add)

            if order.billing_add != Address.objects.get(id=bill_add):
                order.billing_add = Address.objects.get(id=bill_add)
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

            data = {
                        'message': "Order updated successfully.",
                        'url': get_secured_url(
                            self.request) + self.request.META["HTTP_HOST"] + '/orders/' + str(order.id) + '/order-details'
                    }
            return JsonResponse(data)
        

class ChangeDispatchStatusOfOrderOfChild(View):

    def get(self,request, id):
        status = request.GET.get("status", None)
        obj = OrderOfProduct.objects.get(id=id)
        obj.dispatch_status = status
        if DispatchStatus.DISPATCHED.value == status:
            obj.dispatch_date = datetime.now()
            obj.status = OrderStatus.IN_TRANSPORT.value
        obj.save()

        # Main Order sheet Changes
        all_order = OrderOfProduct.objects.filter(order=obj.order).count()
        dispatch_total = OrderOfProduct.objects.filter(order=obj.order, dispatch_status=DispatchStatus.DISPATCHED.value).count()
        if all_order == dispatch_total:
            main_order = OrderDetails.objects.get(id = obj.order.id)
            main_order.dispatch_status = DispatchStatus.DISPATCHED.value
            main_order.dispatch_date = datetime.now()
            main_order.order_status = OrderStatus.IN_TRANSPORT.value
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
        products = OrderOfProduct.objects.filter(order=order,dispatch_status=DispatchStatus.READY.value)

        context = {
            "order_details" : order,
            "products" : products,
        }
        return render(request, self.template_name, context)
    
    def post(self,request, id):
        order = OrderDetails.objects.get(id=id)
        products = OrderOfProduct.objects.filter(order=order,dispatch_status=DispatchStatus.READY.value)
        for i in products:
            # i.lr_no = request.POST.get('lr_no')
            i.transport_compny = request.POST.get('transport_compny')
            i.invoice_no = request.POST.get('invoice_no')
            i.billing_add = order.billing_add
            i.shipped_add = order.shipped_add
            i.save()
            
        data = {
                    'message': "Ready To Dispatch order.",
                    'url': get_secured_url(
                        self.request) + self.request.META["HTTP_HOST"] + '/orders/'+ str(order.id) +'/order-details'
                }
        return JsonResponse(data)


class ExportDispatchNote(View):

    template_name = "orders/dispatch_note.html"
    # template_name = 'my_template.html'

    def get(self, request, id):
        # You can pass context data if needed
        order = OrderDetails.objects.get(id=id)
        products = OrderOfProduct.objects.filter(dispatch_status=DispatchStatus.READY.value)
        context_data = {'variable': 'Hello, World!',
                            "order_details" : order,
                            "products" : products,
                        }

        # Render the template as PDF
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            filename='output.pdf',
            context=context_data,
            show_content_in_browser=False,
            cmd_options={'margin-top': 10},  # Optional: Set additional wkhtmltopdf options
        )

        return response
    
class AddLRNo(View):
    template_name = "orders/panding_lr_list.html"

    def get(self,request):
        order_list=OrderOfProduct.objects.get_pending_lr_no()

        context = {
            'list':order_list
        }
        return render(request, self.template_name, context)
    
    def post(self,request):

        if is_ajax(request):
            lr_no = request.POST.get('lr_no')
            invoice_no = request.POST.get('invoice_no')
            order_list=OrderOfProduct.objects.filter(invoice_no = invoice_no)
            main_order_id = order_list.first().order.id
            for i in order_list:
                i.lr_no = lr_no
                i.save()            
        data = {
                    'message': "Ready To Dispatch order.",
                    'url': get_secured_url(
                        self.request) + self.request.META["HTTP_HOST"] + '/orders/'+ str(main_order_id) +'/order-details'
                }
        return JsonResponse(data)

class ChangeOrderConfirmationStatus(View):

    def get(self,request,id):
        status = request.GET.get("status", None)
        remark = request.GET.get("remark", None)
        order = OrderDetails.objects.get(id=id)
        if order.order_confirmation != OrderConfirmation.CONFIRMED.value and request.user.role != Roles.SUPER_ADMIN.value:
            order.order_confirmation = status
            order.order_confirmation_remark = remark
            order.save()
        elif request.user.role == Roles.SUPER_ADMIN.value: 
            order.order_confirmation = status
            order.order_confirmation_remark = remark
            order.save()
        return redirect("orders:orders-list")
    

class OrderOfProductCancleation(View):

    def get(self, request, id):
        order_of_item = OrderOfProduct.objects.single_order_of_product(id)
        if order_of_item:
            order_of_item.is_active = False
            order_of_item.updated_by = request.user.id
            order_of_item.save()

        return redirect(get_secured_url(
                        self.request) + self.request.META["HTTP_HOST"] + '/orders/'+ str(order_of_item.order.id) +'/order-details')


    
    


    # def post(self, request):
    #     orderofproduct = OrderOfProduct.objects.get(id=id)
    #     orderofproduct.lr_no = request.POST.get('lr_no')
    #     return redirect('orders:order-details', id = orderofproduct.order.id)
    

    
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


