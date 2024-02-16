from django.db import models
from django.db.models import F, ExpressionWrapper, fields, Sum

from decimal import Decimal


class PurchaseOrderManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().order_by("-created_at")
    
    def active(self):
        return self.filter(is_active=True)
    
    def get_po(self,id):
        return self.active().get(pk=id)

    def calculate_and_save_total(self,id):
        try:
            po = self.get_po(id)
            po.total = po.purchaseitem_set.all().aggregate(total=Sum(ExpressionWrapper(F('price') * F('qty'),output_field=fields.FloatField())))['total']
            po.save()
            return True
        except:
            return None

    def calculate_tax_and_save(self, id):
        try:
            po = self.get_po(id)
            total_tax_amount = po.tax_code.aggregate(total_tax_amount=Sum(ExpressionWrapper(F('value') * po.total / 100, output_field=fields.DecimalField())))['total_tax_amount']
            # Ensure that the 'total_tax_amount' is a Decimal
            total_tax_amount = Decimal(total_tax_amount) if total_tax_amount is not None else Decimal(0)
            # Update the 'with_tax_total' field in the PurchaseOrder model
            po.with_tax_total = total_tax_amount + po.total
            po.save()       
            return True
        except:
            return None
        
    def get_po_by_po_no(self,po_no):
        try:
            return self.active().get(po_no=po_no)
        except:
            return None
        
