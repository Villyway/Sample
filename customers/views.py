from django.shortcuts import render, redirect

# Create your views here.
from datetime import datetime

from django.views.generic import View
from django.contrib import messages
from django.db import transaction
from django.views.generic.edit import FormView
from django.http import HttpResponse, JsonResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string

from .forms import CustomerForm, CustomerAddressDetails
from utils.views import get_secured_url, is_ajax
from customers.models import Customer
from utils.models import Address, City, State, Country


# Dashboard
class Dashboard(View):
    template_name = "customers/dashboard.html"

    def get(self,request):
        total = Customer.objects.active().count()
        context = {
            "total":total
        }
        return render(request,self.template_name, context)
    

# Customer List
class CustomerList(View):

    template_name = "customers/list.html"

    def get(self,request):
        customers = Customer.objects.all().order_by('-created_at')

        results_per_page = 10
        page = request.GET.get('page', 1)
        paginator = Paginator(customers, results_per_page)
        try:
            customers = paginator.page(page)
        except PageNotAnInteger:
            customers = paginator.page(1)
        except EmptyPage:
            customers = paginator.page(paginator.num_pages)
        
        context = {
            "customers":customers
        }

        return render(request,self.template_name, context)


# Create customer
class CreateCustomer(FormView):

    template_name = "customers/create.html"
    form_class = CustomerForm
    success_url = "/orders/dashboard/"

    def form_invalid(self, form):
        response = super(CreateCustomer, self).form_invalid(form)
        if is_ajax(self.request):
            data = form.errors
            return JsonResponse(data, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(CreateCustomer, self).form_valid(form)
        try:
            if is_ajax(self.request):
                form_data = form.cleaned_data
                
                with transaction.atomic():
                    customer = Customer()
                    customer.name = form_data['name']
                    customer.mobile = form_data['mobile1']
                    customer.email = form_data['email']
                    customer.contect_person = form_data['person_name']
                    customer.mobile1 = form_data['mobile2']
                    customer.gst_no = form_data['gst_no']
                    customer.created_by = self.request.user.id
                    customer.category = form_data['category']
                    customer.save()                    
                    
                    messages.success(
                        self.request, "Customer added successfully.")
                    success_url = get_secured_url(
                            self.request) + self.request.META["HTTP_HOST"] + '/customers/ '+ str(customer.id) +'/show'
                data = {
                        'message': "customer added successfully.",
                        'url': success_url.replace(" ","")
                    }
                return JsonResponse(data)
            else:
                return response
        
        except Exception as e:
            data = {"error": str(e), "status": 403}
            return JsonResponse(data)


## Address View for State dropdown
class CustomerOfAddress(View):

    def get(self, request, id):
        customer = Customer.objects.get(id)
        address = customer.address.all()
        data = {
            "address": address
        }
        return JsonResponse(data)
    

# Customer Show and their add Address 
class SingleCustomerAndAddAddress(View):

    template_name = "customers/show.html"
    form_class = CustomerAddressDetails

    def get(self, request, id):
        if Customer.objects.filter(id = id).exists():
            customer = Customer.objects.get(id = id)
            context = {
                "customer":customer,
                "form" : self.form_class
            }
            return render(request,self.template_name, context)
        
    def post(self, request, id):

        try:
            if Customer.objects.filter(id = id).exists():
                customer = Customer.objects.get(id = id)
                form_data = self.form_class(request.POST)
                with transaction.atomic():
                    if form_data.is_valid():
                        form_data = form_data.cleaned_data
                        address = Address()
                        address.contect_person = form_data['person_name']
                        address.contect_phone = form_data['mobile1']
                        address.street = form_data["street"]
                        address.street2 = form_data["street2"]
                        if form_data["country"].name == 'Other':
                            address.country = Country.objects.crate_country(form_data["other_country"])
                        else:
                            address.country = form_data["country"]

                        if form_data["state"].name == 'Other':
                            address.state = State.objects.create_state(form_data["other_state"], address.country)
                        else:
                            address.state = form_data["state"]

                        if form_data["city"].name == 'Other':
                            address.city = City.objects.create_city(form_data["other_city"], address.state)
                        else:
                            address.city = form_data["city"]
                        address.zip = form_data["pincode"]
                        address.created_by = request.user.id
                        address.save()
                        customer.address.add(address)
                        address.created_by = self.request.user.id
                        messages.success(request, "Customer of Address Successfully Add!!")
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            else:
                messages.error(
                        request, "Customer was Not Found"
                    )
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            
        except Exception as e:
            messages.error(request, str(e))
            return redirect(request.META['HTTP_REFERER'])


class EditCustomer(FormView):
    template_name = "customers/edit.html"
    form_class = CustomerForm
    success_url = "/customers/dashboard/"

    def get_form_kwargs(self):
        customer = Customer.objects.get(
            id= self.kwargs["id"])
        kwargs = super(EditCustomer, self).get_form_kwargs()
        kwargs.update({"customer": customer, "edit": True})
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(EditCustomer, self).get_context_data(**kwargs)
        customer = Customer.objects.get(id=self.kwargs["id"])
        context['customer'] = customer
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        return context
    
    def form_invalid(self, form):
        response = super(EditCustomer, self).form_invalid(form)
        if is_ajax(self.request):
            data = form.errors
            return JsonResponse(data, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(EditCustomer, self).form_valid(form)
        form_data = form.cleaned_data
        try:
            if is_ajax(self.request):
                                                
                with transaction.atomic():
                    customer = Customer.objects.get(id = self.kwargs['id'])
                    if customer.name != form_data['name']:
                        customer.name = form_data['name']

                    if customer.mobile != form_data['mobile1']:
                        customer.mobile = form_data['mobile1']

                    if customer.email != form_data['email']:
                        customer.email = form_data['email']
                    
                    if customer.contect_person != form_data['person_name']:
                        customer.contect_person = form_data['person_name']
                    
                    if customer.mobile1 != form_data['mobile2']:
                        customer.mobile1 = form_data['mobile2']
                    
                    if customer.gst_no != form_data['gst_no']:
                        customer.gst_no = form_data['gst_no']
                    
                    customer.updated_by = self.request.user.id
                    customer.save()                    
                                            
                    messages.success(
                        self.request, "Customer added successfully.")
                    success_url = get_secured_url(
                            self.request) + self.request.META["HTTP_HOST"] + '/customers/ '+ str(customer.id) +'/show'
                data = {
                        'message': "customer added successfully.",
                        'url': success_url.replace(" ","")
                    }
                return JsonResponse(data)
            else:
                return response
        
        except Exception as e:
            data = {"error": str(e), "status": 403}
            return JsonResponse(data)
        

# Search Vendor
class SearchCustomer(View):
    template_name = "components/customer-list.html"

    def get(self, request):
        try:
            if is_ajax(request):
                query = request.GET.get("query", None)
                customers = Customer.objects.search(query)

                results_per_page = 100
                page = request.GET.get('page', 1)
                paginator = Paginator(customers, results_per_page)
                try:
                    customers = paginator.page(page)
                except PageNotAnInteger:
                    customers = paginator.page(1)
                except EmptyPage:
                    customers = paginator.page(paginator.num_pages)
                html = render_to_string(
                    template_name=self.template_name,
                    context={"customers": customers}
                )

                data_dict = {
                    "data": html
                }
                return JsonResponse(data=data_dict, safe=False)
                
            else:
                return redirect("customers:dashboard")
        except Exception as e:
            return JsonResponse({"error": str(e)})
