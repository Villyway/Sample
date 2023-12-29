import datetime

from itertools import chain

from django.db import models
from django.db.models import Q
from django.db.models import Sum, Count


class CustomerManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()
    
    def active(self):
        return self.filter(is_active=True)
    
    def customer_wise_total_orders(self):
        customer_list = self.annotate(total_orders=Count('orderdetails'))
        if customer_list:
            customers = []
            orders = []
            for i in customer_list:
                customers.append(i.name)
                orders.append(i.total_orders)
            return customers, orders
    
    