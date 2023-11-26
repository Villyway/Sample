import datetime

from itertools import chain

from django.db import models
from django.db.models import Q
from django.db.models import Sum

from utils.constants import OrderStatus, DispatchStatus


class OrdersDetailsManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()
    
    def active(self):
        return self.filter(is_active=True)
    
    def total_order(self):
        return self.active().count()
    
    def total_deleverd(self):
        return self.active().filter(order_status = OrderStatus.DELIVERED.value).count()
    
    def total_orders_in_transport(self):
        return self.active().filter(order_status = OrderStatus.IN_TRANSPORT.value).count()
    
    def total_panding_order(self):
        return self.active().filter(order_status = OrderStatus.PENDING.value).count()
    
    
class OrderOfProductManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().order_by("-created_at")


    def get_queryset(self):
        return super().get_queryset().order_by("-created_at")
    
    def active(self):
        return self.filter(is_active=True)
    
    def panding(self):
        return self.active().filter(dispatch_status = DispatchStatus.PENDING.value).count()
    
    def underprocess(self):
        return self.active().filter(dispatch_status = DispatchStatus.UNDER_PROCESS.value).count()
    
    def ready(self):
        return self.active().filter(dispatch_status = DispatchStatus.READY.value).count()
    
    def dispatched(self):
        return self.active().filter(dispatch_status = DispatchStatus.DISPATCHED.value).count()
    
    def total_deleverd(self):
        return self.active().filter(status = OrderStatus.DELIVERED.value).count()
    
    def total_orders_in_transport(self):
        return self.active().filter(status = OrderStatus.IN_TRANSPORT.value).count()
    
    def total_panding_order(self):
        return self.active().filter(status = OrderStatus.PENDING.value).count()
    
