import datetime

from itertools import chain

from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.db import models
from django.db.models import Q
from django.db.models import Sum, Count, Avg


from utils.constants import OrderStatus, DispatchStatus, OrderConfirmation



class OrdersDetailsManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()
    
    def active(self):
        return self.filter(is_active=True)
    
    def get_order(self,id):
        try:
            return self.get(id=id)
        except:
            return None
        
    
    def orders(self, count=False):
        if count:
            return self.active().count()
        else:
            return self.active().order_by('-order_no')
    
    def oders_filtered_by_status(self, status, count=False):
        if count:
            return self.active().filter(order_status = status).count()
        else:
            return self.active().filter(Q(order_status = status) | Q(orderofproduct__status=status))
        
    def oders_filtered_by_dispatch_status(self, status, count=False):
        if count:
            return self.active().filter( dispatch_status= status).count()
        else:
            return self.active().filter(dispatch_status = status)
        
    def orders_filtered_by_confirmation(self, status, count=False):
        if count:
            return self.active().filter(order_confirmation = status).count()
        else:
            return self.active().filter(order_confirmation = status)
        
    def singel_order_by_order_no(self, order_no):
        try:
            return self.active().get(order_no = order_no)
        except:
            return None
        
    def today_orders(self,count=True):
        today = datetime.datetime.now().date()
        if count:
            return self.filter(date=today).count()
        else:
            return self.filter(date=today)
        
    
    def search1(self, query=None, dates=None, dispatch_status=None, order_status=None):
        
        if query == None and dispatch_status and 'choose'and order_status=='choose':
            return self.filter(date__range=dates)        
        elif query:
            if order_status != 'choose' and dispatch_status != 'choose':
                return self.filter(dispatch_status=dispatch_status,order_status=order_status).filter(Q(customer__name__icontains=query) | Q(order_no__icontains=query),date__range=dates)
            
            elif dispatch_status != 'choose':
                return self.oders_filtered_by_dispatch_status(dispatch_status).filter(Q(orderofproduct_set__dispatch_status__icontains=dispatch_status)|Q(customer__name__icontains=query) | Q(order_no__icontains=query),date__range=dates)
            
            elif order_status != 'choose':

                return self.oders_filtered_by_status(order_status).filter(Q(customer__name__icontains=query) | Q(order_no__icontains=query),date__range=dates)
            else:
                return self.active().filter(Q(customer__name__icontains=query) | Q(order_no__icontains=query),date__range=dates)
        else:
            if dispatch_status != 'choose':
                return self.oders_filtered_by_dispatch_status(dispatch_status).filter(Q(customer__name__icontains=query) | Q(order_no__icontains=query),date__range=dates)
            
            elif order_status != 'choose':
                return self.oders_filtered_by_status(order_status).filter(Q(customer__name__icontains=query) | Q(order_no__icontains=query),date__range=dates)
            
            elif order_status != 'choose' and dispatch_status != 'choose':
                return self.filter(dispatch_status=dispatch_status,order_status=order_status).filter(Q(customer__name__icontains=query) | Q(order_no__icontains=query),date__range=dates)
            
            else:
                return self.orders()

    def search(self, query=None, dates=None, dispatch_status=None, order_status=None):
        if dates is None:
            raise ValueError("Dates must be provided.")

        base_queryset = self.filter(date__range=dates)

        if dispatch_status == 'choose' and order_status == 'choose':
            return base_queryset

        q_objects = Q(customer__name__icontains=query)

        if query:
            base_queryset = base_queryset.filter(q_objects)

        if dispatch_status != 'choose':
            base_queryset = base_queryset.filter(Q(dispatch_status=dispatch_status) | Q(orderofproduct__dispatch_status=dispatch_status))

        if order_status != 'choose':
            base_queryset = base_queryset.filter(order_status=order_status)

        return base_queryset.distinct()


    # def search(self, query=None, dates=None, dispatch_status=None, order_status=None):
    #     # Ensure that the dates are provided
    #     if dates is None:
    #         raise ValueError("Dates must be provided.")

    #     # Create a base queryset with the date range
    #     base_queryset = self.filter(date__range=dates)

    #     # Check for dispatch_status and order_status
    #     if dispatch_status == 'choose' and order_status == 'choose':
    #         return base_queryset

    #     # Start building the queryset based on conditions
    #     if query:
    #         q_objects = Q(customer__name__icontains=query) | Q(order_no__icontains=query)
    #         base_queryset = base_queryset.filter(q_objects)

    #     if dispatch_status != 'choose':
    #         base_queryset = base_queryset.filter(orderofproduct_set__dispatch_status__icontains=dispatch_status)

    #     if order_status != 'choose':
    #         base_queryset = base_queryset.filter(order_status=order_status)

    #     return base_queryset.distinct()
        
    # def order_search(self, query=None, dates=None, dispatch_status=None, order_status=None):

    #     if query:
    #         if dispatch_status !='choose' and order_status != 'choose':
    #             return self.active().filter(prderofproduct__status=order_status,prderofproduct__dispatch_status=dispatch_status)
    #         elif dispatch_status !='choose'


class OrderOfProductManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().order_by("-created_at")


    def get_queryset(self):
        return super().get_queryset().order_by("-created_at")
    
    def active(self):
        return self.filter(is_active=True)
    
    def single_order_of_product(self, id):
        try:
            return self.active().get(id=id)
        except:
            return None
    
    def get_list_by_status(self, status, count=False):

        dispatch_status_list = [i.value for i in DispatchStatus]
        order_status_list = [i.value for i in OrderStatus]
        if status in dispatch_status_list:
            if count:
                return self.active().filter(dispatch_status = status).count()
            else:
                return self.active().filter(dispatch_status = status)
        elif status in order_status_list:
            if count:
                return self.active().filter(status = status).count()
            else:
                return self.active().filter(status = status)
        else:
            return None
        
    def get_pending_lr_no(self):
        return self.active().filter(~Q(status = OrderStatus.DELIVERED.value),lr_no=None,invoice_no__isnull=False,transport_compny__isnull=False).values_list('order__date','order__order_no', 'order__customer__name', 'transport_compny', 'invoice_no','dispatch_date').distinct()
    
    def top_products(self):
        return self.active().values('product').annotate(total_quantity_ordered=Sum('order_qty'))
    
    def get_pending_orders(self):
        return self.active().filter(~Q(status = OrderStatus.DELIVERED.value))
    
    def search(self, query=None, dates=None, dispatch_status=None, order_status=None):
        if dates is None:
            base_queryset = self.active()
        else:
            base_queryset = self.active().filter(created_at__range=dates)

        if dispatch_status == 'choose' and order_status == 'choose':
            return base_queryset

        q_objects = Q(customer__name__icontains=query)

        if query:
            base_queryset = base_queryset.filter(q_objects)

        if dispatch_status != 'choose':
            base_queryset = base_queryset.filter(Q(dispatch_status=dispatch_status))

        if order_status != 'choose':
            base_queryset = base_queryset.filter(status=order_status)
        
        if order_status != 'choose' and dispatch_status != 'choose':
            base_queryset = base_queryset.filter(status=order_status,dispatch_status=dispatch_status)

        return base_queryset.distinct()
    
    def get_monthly_order_of_product_with_total_qty(self):
      
        table_data = {}
        monthly_product_totals = self.active().filter(
            order__created_at__isnull=False  # Assuming 'OrderDetails' has a 'created_at' field
            ).annotate(
            month=TruncMonth('order__created_at')
            ).values(
                'month',
                'product__name',
                'product__code',  # Assuming 'Product' has a 'name' field
            ).annotate(
                total_qty=Sum('order_qty')
            ).order_by('month', 'product__name')
        
        all_months = set(item['month'] for item in monthly_product_totals)
        all_months = sorted(all_months)
        
        # monthly_totals_dict = {item['month']: item['total_qty'] for item in monthly_product_totals}
        table_data = {}

        for entry in monthly_product_totals:
            product_code = entry['product__code']
            product_name = entry['product__name']+ ',' + entry['product__code']
            month = entry['month']
            total_qty = entry['total_qty']
        
            if product_name not in table_data:
                table_data[product_name] = {}
                
        
            table_data[product_name][month] = total_qty
            #table_data['code'] = product_code

        # Ensure all months are included in the data with quantity 0 for products that didn't sell
        for product_name in table_data:
            for month in all_months:
                if month not in table_data[product_name]:
                    table_data[product_name][month] = 0
        
        table_rows = [{'product_code':product_name.split(',')[1],'product_name': product_name.split(',')[0],
                        'monthly_data': dict(sorted(data.items()))} for product_name, data in table_data.items()]

        return table_data, table_rows
    
    def product_wise_average_orders(self):

        return self.active().values('product__code').annotate(avg_order_qty=Avg('order_qty'))
    
    def get_so_no_by_product(self,so_no):
        return self.active().filter(order__order_no=so_no)

        # return self.active().filter(order__created_at__isnull=False).annotate(month=TruncMonth('order__created_at')).values('month').annotate(total_qty=Sum('order_qty')).order_by('month')
