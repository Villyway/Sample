from django.db import models


class PurchaseOrderManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().order_by("-created_at")

    def calculate_and_save_total(self):

        items = self.purchaseitem_set.all()
        total = 0
        for item in items:
            prise = item.price * item.qty
            total =  total + prise
        po = item.po
        po.total=total
        po.save()

    def calculate_tax_and_save(self):

        items = self.purchaseitem_set.all()
        total = 0
        for item in items:
            prise = item.price * item.qty
            total =  total + prise
        po = item.po
        po.total=total
        po.save()







