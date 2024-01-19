from django.db import models

from products.models import Product
from vendors.models import Vendor
from base.models import Base


# Create your models here.

# class TaxCode(Base):
#     name = models.CharField(max_length=150, blank=True, null=True) 
#     code= models.CharField(max_length=30, blank=True, null=True)
#     value =  models.DecimalField(max_digits=5, decimal_places=2)

# class PaymentTerms(Base):
#     name = models.CharField(max_length=150, blank=True, null=True) 
#     description = models.TextField(blank=True, null=True)

# class PurchaseOrder(Base):
#     po_no = models.CharField(max_length=30, blank=True, null=True)
#     vendor = models.ForeignKey(
#         Vendor, on_delete=models.CASCADE)
#     part = models.ManyToManyField(
#         Product, on_delete=models.CASCADE)
#     qty = models.DecimalField(max_digits=10, decimal_places=2)
#     tax_code = models.ForeignKey(
#         TaxCode, on_delete=models.CASCADE)
#     status = models.BooleanField(default=False)
#     del_date = models.DateTimeField(blank=True, null=True)
#     total = models.DecimalField(max_digits=5, decimal_places=2)
#     with_tax_total = models.DecimalField(max_digits=5, decimal_places=2)
#     checked_by = models.IntegerField(null=True, blank=True)
#     remarks = models.TextField(blank=True, null=True)


