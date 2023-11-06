from django.shortcuts import render

# Create your views here.
from datetime import datetime

from django.views.generic import View
from django.contrib import messages
from django.db import transaction
from django.views.generic.edit import FormView
from django.http import HttpResponse, JsonResponse, Http404

from orders.forms import OrdersForm
from utils.views import get_secured_url, is_ajax


class Dashboard(View):
    template_name = "orders/dashboard.html"

    def get(self,request):

        return render(request,self.template_name)
    

# Create Customer
class CreateOrders(FormView):
    
    template_name = "orders/create.html"
    form_class = OrdersForm
    success_url = "/orders/dashboard/"

    def form_invalid(self, form):
        response = super(CreateOrders, self).form_invalid(form)
        if is_ajax(self.request):
            data = form.errors
            return JsonResponse(data, status=400)
        else:
            return response

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


