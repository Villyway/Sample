import json

from django.shortcuts import render, redirect

# Create your views here.
from datetime import datetime
import operator
import requests

from django.views.generic import View
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string

from utils.views import get_secured_url, is_ajax, generate_order_dispatch_no
from customers.models import Customer
from products.models import Product
from orders.models import OrderDetails, OrderOfProduct
from utils.constants import PackingType, OrderUOM, OrderStatus, DispatchStatus, OrderConfirmation, Roles, OrdersType, StockTransection
from utils.models import Address
from utils.views import send_email
from orders.resources import OrderReport
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from inventry.models import SimpleStockUpdte

from wkhtmltopdf.views import PDFTemplateResponse

class Dashboard(View):
    template_name = "orders/dashboard.html"

    def get_top_10_products(self):
        # Aggregate the total quantity ordered for each product
        top_products = OrderOfProduct.objects.top_products()

        # Order the products by total quantity ordered in descending order
        top_products = top_products.order_by('-total_quantity_ordered')[:10]

        # Retrieve the actual Product instances for the top products
        top_product_ids = [item['product'] for item in top_products]
        top_10_products = Product.objects.filter(id__in=top_product_ids)

        # Add the total quantity ordered to each product in the list
        for product in top_10_products:
            product.total_quantity_ordered = next(item['total_quantity_ordered'] for item in top_products if item['product'] == product.id)

        return sorted(top_10_products,key=operator.attrgetter('total_quantity_ordered'),reverse=True)  #sorted(auths, key=operator.attrgetter('last_name'))

    def get(self,request):
        hold_orders = OrderDetails.objects.orders_filtered_by_confirmation(OrderConfirmation.HOLD.value,True)
        confirm_orders = OrderDetails.objects.orders_filtered_by_confirmation(OrderConfirmation.CONFIRMED.value,True)
        today_orders = OrderDetails.objects.today_orders(True)
        customer_list = Customer.objects.filter(is_active=True).values('name')
        customers,orders = Customer.objects.customer_wise_total_orders()
        top_10_products = self.get_top_10_products()

        table_rows, table_data = OrderOfProduct.objects.get_monthly_order_of_product_with_total_qty()
        months = sorted(set(month for data in table_rows.values() for month in data))

        #Order of products.       
        context = {
            "hold_orders":hold_orders,
            "confirm_orders" : confirm_orders,
            "today_orders":today_orders,
            "customers":customers,
            "orders" : orders,
            "top_10_products" :top_10_products,
            'table_rows': table_data,
            'months': months,
            
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
            'packaging_type' : [e.value for e in PackingType],
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
        results_per_page = 10
        page = request.GET.get('page', 1)
        paginator = Paginator(orders, results_per_page)
        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)
        
            
        context = {
            "orders": orders,
            "data" : [page,results_per_page],
            "confirm_status": [i.value for i in OrderConfirmation],
            "order_status": [i.value for i in OrderStatus],
            "order_dispatch_status": [i.value for i in DispatchStatus],
            }
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
        
        message = {
                    "name": order.customer.name,
                    "order_no": order.order_no,
                    "order_date":order.date,
                    "shipping_address":order.shipped_add,
                    "order_status":order.order_status,
                    "dispatch_status":order.dispatch_status,
                    }
        
        # send_email(order.customer, message,
                            #    "order_conformation_status_email.html", self.request,"Order Confirmation")
            
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
                
        elif DispatchStatus.READY.value == status:
            with transaction.atomic():
                if obj.product.stock >= obj.order_qty:
                    # product = obj.product
                    # stock = SimpleStockUpdte()
                    # stock.part = obj.product
                    # stock.old_stock = obj.product.stock
                    # stock.received_by = obj.order.customer.name
                    # stock.received_qty = obj.order_qty
                    # stock.transection_type = StockTransection.DR.value
                    # stock.quantity_on_hand = obj.product.stock - obj.order_qty
                    # stock.save()
                    # product.stock = stock.quantity_on_hand
                    # product.save()
                    obj.save()
                else:
                    messages.error(
                        self.request, "Stock is Not Availabel.")
                    obj.save()
        else:
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
        
        # data = {
        #             'message': message_string,
        #             'url': get_secured_url(
        #                 self.request) + self.request.META["HTTP_HOST"] + 'orders/'+ str(obj.order.id) +'/order-details'
        #         }
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
        products = OrderOfProduct.objects.filter(dispatch_status=DispatchStatus.READY.value, order=order)
        context_data = {'variable': 'Hello, World!',
                            "order_details" : order,
                            "products" : products,
                            "title" : "DESPATCH NOTE"
                        }

        # Render the template as PDF
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            filename='output.pdf',
            context=context_data,
            show_content_in_browser=False,
            cmd_options={'margin-top': 10, 'orientation': 'Landscape'},# Optional: Set additional wkhtmltopdf options
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


# Change Conformation Status
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
    

# Order Cancleation
class OrderOfProductCancleation(View):

    def get(self, request, id):
        order_of_item = OrderOfProduct.objects.single_order_of_product(id)
        if order_of_item:
            order_of_item.is_active = False
            order_of_item.updated_by = request.user.id
            order_of_item.save()

        return redirect(get_secured_url(
                        self.request) + self.request.META["HTTP_HOST"] + '/orders/'+ str(order_of_item.order.id) +'/order-details')


# Order Report
class OrdersReport(View):
    template_name = "orders/report.html"

    def get(self, request):
        context = {
            "confirm_status": [i.value for i in OrderConfirmation],
            "order_status": [i.value for i in OrderStatus],
            "order_dispatch_status": [i.value for i in DispatchStatus],
            }

        return render(request,self.template_name,context)
    

#Export Data
class ExportData(View):
    
    def get(self, request):
        query = request.GET.get("query", None)
        start_date = request.GET.get("start", OrderDetails.objects.all().first().date)
        end_date = request.GET.get("end", OrderDetails.objects.last().date)

        if start_date != '':
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        else:
            start_date = None

        if end_date != '':
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        else:
            end_date = None
                        
        if start_date != None and end_date != None:
            dates = [start_date,end_date]
        else:
            dates = None

        dispatch_status = request.GET.get("dispatch_status", None)
        order_status = request.GET.get("order_status", None)

        products = OrderOfProduct.objects.search(query, dates, dispatch_status, order_status)

        order_resourse = OrderReport()
        dataset = order_resourse.export(products)
        response = HttpResponse(dataset.csv,content_type="text/csv")
        time_name = datetime.now().strftime("%Y%m%d_%H_%M_%S")
        response['Content-Disposition'] = 'attachment; filename="orders_report'+ time_name + '".csv"'
        return response


# Order Custome Report
class OrdersCustomReportResponse(View):
    template_name = "components/search-report.html"

    def get(self,request):
        try:
            if is_ajax(request):
                query = request.GET.get("query", None)
                start_date = request.GET.get("start", OrderDetails.objects.all().first().date)
                end_date = request.GET.get("end", OrderDetails.objects.last().date)

                if start_date != '':
                    start_date = datetime.strptime(start_date, '%Y-%m-%d')
                else:
                    start_date = None

                if end_date != '':
                    end_date = datetime.strptime(end_date, '%Y-%m-%d')
                else:
                    end_date = None
                    
                if start_date != None and end_date != None:
                    dates = [start_date,end_date]
                else:
                    dates = None

                dispatch_status = request.GET.get("dispatch_status", None)
                order_status = request.GET.get("order_status", None)

                products = OrderOfProduct.objects.search(query, dates, dispatch_status, order_status)

                html = render_to_string(
                    template_name=self.template_name,
                    context={"ordersofproducts": products}
                )
                data_dict = {
                    "data": html
                }
                return JsonResponse(data=data_dict, safe=False)
            # if request.META.get('HTTP_REFERER'):
            #     return redirect(request.META.get('HTTP_REFERER'))
            # else:
            #     return redirect("products:list")
        except Exception as e:
            return JsonResponse({"error": str(e)})


# OrderSearch
class OrderSearch(View):
    template_name = "components/search-orders.html"

    def get(self, request):
        try:
            if is_ajax(request):
                query = request.GET.get("query", None)
                start_date = request.GET.get("start", OrderDetails.objects.all().first().date)
                end_date = request.GET.get("end", OrderDetails.objects.all().last().date)
                if start_date != '':
                    start_date = datetime.strptime(start_date, '%Y-%m-%d')
                else:
                    start_date = OrderDetails.objects.first().date

                if end_date != '':
                    end_date = datetime.strptime(end_date, '%Y-%m-%d')
                else:
                    end_date = OrderDetails.objects.last().date

                dispatch_status = request.GET.get("dispatch_status", None)
                order_status = request.GET.get("order_status", None)
                orders = OrderDetails.objects.search(query, [start_date,end_date], dispatch_status, order_status)
                results_per_page = 100
                page = request.GET.get('page', 1)
                paginator = Paginator(orders, results_per_page)
                try:
                    orders = paginator.page(page)
                except PageNotAnInteger:
                    orders = paginator.page(1)
                except EmptyPage:
                    orders = paginator.page(paginator.num_pages)
                html = render_to_string(
                    template_name=self.template_name,
                    context={"orders": orders}
                )
                data_dict = {
                    "data": html
                }

                return JsonResponse(data=data_dict, safe=False)

            if request.META.get('HTTP_REFERER'):
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                return redirect("orders:orders-list")
        except Exception as e:
            return JsonResponse({"error": str(e)})


# Track Lr No
class TrackLR(View):
    
    template_name = "orders/track.html"

    def get(self,request,id):
        order = OrderDetails.objects.get_order(id)
        lr_nos = []
        if order:
            order_of_products = order.orderofproduct_set.all()
            
            for i in order_of_products:
                if i.lr_no not in lr_nos:
                    lr_nos.append([i.lr_no,i.transport_compny])

        api_url_vrl = 'https://www.vrlgroup.in/track_consignment.aspx?lrtrack=1&lrno='
        
        try:
            track_details = []
            for i in lr_nos:
                if i:
                    if i[1]=='VRL':
                        # Make a GET request to the API
                        response = requests.post(api_url_vrl + i[0])
                        # Check if the response status is OK (status code 200-299)
                        response.raise_for_status()
                        # Parse the JSON response
                        api_data = response.json()
                        track_details.append(api_data)
                    # Do something with the API data
                    # ...
                    elif i[1] == 'DHL':
                        response = requests.get('https://erp.krunalindustries.com/dhl/'+ order.order_no +'/track-order/')
                        
                        # data_string = response.decode('utf-8')
                        data_dict = response.json()
                        status = data_dict['status']
                        message = data_dict['message']
                        data = data_dict['data']
                        print(data)

                        
            context = {
                "data":track_details
            }
            return render(request,self.template_name,context)
        except requests.exceptions.RequestException as e:
            # Handle any errors that occurred during the API call
            return JsonResponse({'message': f'API call failed: {str(e)}'}, status=500)

