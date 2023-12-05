import datetime

from itertools import chain

from django.db import models
from django.db.models import Q
from django.db.models import Sum, Count


from utils.constants import OrderStatus, DispatchStatus, OrderConfirmation



class OrdersDetailsManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()
    
    def active(self):
        return self.filter(is_active=True)
    
    def orders(self, count=False):
        if count:
            return self.active().count()
        else:
            return self.active().order_by('-date')
    
    def oders_filtered_by_status(self, status, count=False):
        if count:
            return self.active().filter(order_status = status).count()
        else:
            return self.active().filter(order_status = status)
        
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
    
    def get_list_by_dispatch_status(self, status, count=False):

        if count:
            return self.active().filter(dispatch_status = status).count()
        else:
            return self.active().filter(dispatch_status = status)
        
    def get_pending_lr_no(self):
        return self.active().filter(lr_no=None,invoice_no__isnull=False,transport_compny__isnull=False).values_list('order__date','order__order_no', 'order__customer__name', 'transport_compny', 'invoice_no','dispatch_date').distinct()
    
    def top_products(self):
        return self.active().values('product').annotate(total_quantity_ordered=Sum('order_qty'))
    
    
