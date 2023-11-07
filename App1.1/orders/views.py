from django.shortcuts import render, redirect

# Create your views here.
from datetime import datetime

from django.views.generic import View
from django.contrib import messages
from django.db import transaction
from django.views.generic.edit import FormView
from django.http import HttpResponse, JsonResponse, Http404

from orders.forms import OrdersForm
from utils.views import get_secured_url, is_ajax
from customers.models import Customer
from products.models import Product
from orders.models import OrderDetails, OrderOfProduct


class Dashboard(View):
    template_name = "orders/dashboard.html"

    def get(self,request):

        return render(request,self.template_name)
    

class CreateOrders(View):
    template_name = "orders/create.html"
    success_url = "/orders/dashboard/"

    def get(self,request):
        customers = Customer.objects.filter(is_active = True)
        products = Product.objects.finished_product()
        context = {
            'products': products,
            'customers': customers

        }
        return render(request,self.template_name, context)
    
    def post(self, request):
        if is_ajax(self.request):
            with transaction.atomic():

                customer = self.request.POST.get('customers')
                remark = self.request.POST.get('remark')

                if Customer.objects.filter(id=customer).exists():
                    customer_obj = Customer.objects.get(id = customer)

                    order = OrderDetails()
                    order.customer = customer_obj
                    order.date = datetime.today().date()
                    order.remarks = remark
                    order.save()

                    products = self.request.POST.getlist('product[]')
                    quantities = self.request.POST.getlist('quantity[]')
                    for product_name, quantity_value in zip(products, quantities):
                        if Product.objects.by_code(product_name):
                            product = Product.objects.by_code(product_name)
                            order_of_product = OrderOfProduct()
                            order_of_product.order = order
                            order_of_product.product = product
                            order_of_product.order_qty = quantity_value
                            order_of_product.save()
                messages.success(
                    self.request, "Order added successfully.")
            data = {
                    'message': "Order added successfully.",
                    'url': get_secured_url(
                        self.request) + self.request.META["HTTP_HOST"] + '/orders/create-orders'
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



class CreateOrders1(FormView):
    
    template_name = "orders/create.html"
    form_class = OrdersForm
    success_url = "/orders/dashboard/"

    def form_invalid(self, form):
        response = super(CreateOrders, self).form_invalid(form)
        if is_ajax(self.request):
            data = form.errors
            return JsonResponse(data, status=400)
        else:
            return redirect('/redirect-success/')

    def form_valid(self, form):
        response = super(CreateOrders, self).form_valid(form)
        try:
            if is_ajax(self.request):
                form_data = form.cleaned_data
                with transaction.atomic():
                    products = self.request.POST.getlist('product[]')
                    quantities = self.request.POST.getlist('quantity[]')

                    for product_name, quantity_value in zip(products, quantities):
                        print(product_name, quantity_value)

                    
                    messages.success(
                        self.request, "Product added successfully.")
                data = {
                        'message': "Product added successfully.",
                        'url': get_secured_url(
                            self.request) + self.request.META["HTTP_HOST"] + '/products/' + str(1) + '/product-property/'
                    }
                return JsonResponse(data)
            else:
                return response
        
        except Exception as e:
            data = {"error": str(e), "status": 403}
            return JsonResponse(data)


