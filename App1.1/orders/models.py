from django.db import models

from base.models import Base
from products.models import Product, Unit
from utils.models import Address
from utils.constants import OrderStatus, OrderUOM, PackingType, DispatchStatus, OrdersType
from customers.models import Customer
from utils.models import Address
from orders.managers import OrdersDetailsManager, OrderOfProductManager


# Order Details
class OrderDetails(Base):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order_no = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateTimeField(blank=True, null=True)
    order_status = models.CharField(
        max_length=25, choices=OrderStatus.choices(), default=OrderStatus.PENDING.value)
    sales_challan = models.CharField(max_length=80, null=True, blank=True)
    lr_no = models.CharField(max_length=150, null=True, blank=True)
    
    dispatch_date = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    pickup_by_party_date = models.DateTimeField(blank=True, null=True)
    dispatch_status = models.CharField(
        max_length=25, choices=DispatchStatus.choices(), default=DispatchStatus.PENDING.value)
    billing_add = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, related_name="billing_address")
    shipped_add = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, related_name="shipping_address")
    order_type = models.CharField(
        max_length=25, choices=OrdersType.choices(), default=OrdersType.DOMESTIC.value)
    objects = OrdersDetailsManager()

    def __str__(self):
        return self.customer.name


# OrderOfProduct:
class OrderOfProduct(Base):
    order = models.ForeignKey(
        OrderDetails, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True)
    order_qty = models.PositiveIntegerField(default=0)
    uom = models.CharField(
        max_length=25, choices=OrderUOM.choices(), default=OrderUOM.NOS.value)
    packing_type = models.CharField(
        max_length=25, choices=PackingType.choices(), default=PackingType.BOX.value)
    status = models.CharField(
        max_length=25, choices=OrderStatus.choices(), default=OrderStatus.PENDING.value)
    dispatch_status = models.CharField(
        max_length=25, choices=DispatchStatus.choices(), default=DispatchStatus.PENDING.value)
    transport_compny = models.CharField(max_length=150, null=True, blank=True)
    delivery_mode = models.CharField(max_length=150, null=True, blank=True)
    dispatch_date = models.DateTimeField(blank=True, null=True)
    delivered_date = models.DateTimeField(blank=True, null=True)
    billing_add = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, related_name="billing_address_for_single_product")
    shipped_add = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, related_name="shipping_address_for_single_product")
    lr_no = models.CharField(max_length=150, null=True, blank=True)
    invoice_no = models.CharField(max_length=150, null=True, blank=True)

    objects = OrderOfProductManager()
    
    def __str__(self):
        return self.product.name