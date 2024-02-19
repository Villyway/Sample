from django.db import models

from base.models import Base
from purchase.models import PurchaseOrder
from products.models import Product, Unit
from inward.managers import InWordManager

# Create your models here.


class Inward(Base):
    inward_no = models.CharField(max_length=30, blank=True, null=True) # autogenrated
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    remarks = models.TextField(blank=True, null=True)

    objects = InWordManager()

    def __str__(self):
        return self.inward_no


class InwardItems(Base):
    inward = models.ForeignKey(Inward, on_delete=models.CASCADE)
    chalan_no = models.CharField(max_length=30, blank=True, null=True)
    received_date = models.DateTimeField(auto_now_add=True)
    received_item = models.ForeignKey(Product, on_delete=models.CASCADE)
    uom = models.ForeignKey(Unit, on_delete=models.CASCADE)
    qty = models.DecimalField(max_digits=12, decimal_places=4)
    invoice_date = models.DateTimeField()
    qc_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)