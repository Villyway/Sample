from django.db import models

from base.models import Base
from products.models import Product, Unit
from utils.models import Address
from utils.constants import OrderStatus, OrderUOM, PackingType, DispatchStatus
from customers.models import Customer

# # Create your models here.
# class Customer(Base):
#     name = models.CharField(max_length=150, null=True, blank=True)
#     mobile = models.CharField(max_length=50, null=True, blank=True)
#     country_code = models.CharField(max_length=4, default="91")
#     email = models.EmailField(null=True, blank=True)
#     contect_person = models.CharField(max_length=150, null=True, blank=True)
#     address = models.ManyToManyField(Address, blank=True)
#     mobile1 = models.CharField(max_length=50, null=True, blank=True)

#     def __str__(self):
#         return self.name
    

class OrderDetails(Base):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order_no = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateTimeField(blank=True, null=True)
    order_status = models.CharField(
        max_length=25, choices=OrderStatus.choices(), default=OrderStatus.PENDING.value)
    sales_challan = models.CharField(max_length=80, null=True, blank=True)
    lr_no = models.CharField(max_length=150, null=True, blank=True)
    transport_compny = models.CharField(max_length=150, null=True, blank=True)
    dispatch_date = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    pickup_by_party_date = models.DateTimeField(blank=True, null=True)
    dispatch_status = models.CharField(
        max_length=25, choices=DispatchStatus.choices(), default=DispatchStatus.PENDING.value)

    def __str__(self):
        return self.customer.name


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
    
    def __str__(self):
        return self.product.name