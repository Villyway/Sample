from django.db import models

from products.models import Product, Categories
from vendors.models import Vendor
from base.models import Base

from purchase.managers import PurchaseOrderManager


# Create your models here.

class TaxCode(Base):
    name = models.CharField(max_length=150, blank=True, null=True) 
    code= models.CharField(max_length=30, blank=True, null=True)
    value =  models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.name)

class PaymentTerms(Base):
    name = models.CharField(max_length=150, blank=True, null=True) 
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


class TermsAndConditions(Base):
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name)



class PurchaseOrder(Base):
    po_no = models.CharField(max_length=30, blank=True, null=True) # autogenrated
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True,null=True)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE)
    tax_code = models.ManyToManyField(TaxCode, blank=True)
    general_terms = models.ManyToManyField(TermsAndConditions, blank=True)
    payment_term = models.ForeignKey(PaymentTerms, on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=True)
    del_date = models.DateTimeField(blank=True, null=True)
    total = models.DecimalField(max_digits=12,decimal_places=2, default=0)
    with_tax_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    checked_by = models.IntegerField(null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    close_date = models.DateTimeField(blank=True, null=True)
    gl_name = models.ForeignKey(Categories, on_delete=models.CASCADE, blank=True,null=True)

    objects = PurchaseOrderManager()

    def __str__(self):
        return str(self.vendor.comany_name)


class PurchaseItem(Base):
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    part = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.DecimalField(max_digits=12, decimal_places=4)
    del_date = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=12,decimal_places=2, default=0)
    del_status = models.DateTimeField(blank=True, null=True)
    recived_qty = models.DecimalField(max_digits=12, decimal_places=4, default=0)

    def __str__(self):
        return str(self.part.name)
    


