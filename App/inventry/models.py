from django.db import models

from base.models import Base
from products.models import Product, Unit
from vendors.models import Vendor
from utils.views import upload_file
from users.models import User


# Create your models here.

# Inword
class InWord(Base):
    grn_no = models.CharField(max_length=150)
    bill_no = models.CharField(max_length=150)
    bill_date = models.DateField()
    part = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='parts_inword',)
    received_qty = models.CharField(max_length=150)
    uom = models.ForeignKey(
        Unit, on_delete=models.CASCADE)
    in_time = models.TimeField()
    qc_status = models.BooleanField(default=False)
    purchase_order_no = models.CharField(max_length=150)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name='vendor',)
    receive_by = models.CharField(max_length=150)
    remarks = models.TextField(blank=True, null=True)
    file_url = models.URLField(max_length=500, null=True, blank=True)
    old_stock = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.grn_no
    
    def save_image_url(self, file_obj, file_url):
        file_obj = upload_file(self, file_obj,"inward/"+ str(self.vendor.id))
        file_obj = file_url + '/media/' + file_obj
        self.file_url = file_obj
        self.save()
        return True
    

#OutWord
class Outword(Base):
    out_ward_sr_no = models.CharField(max_length=20, unique=True, blank=True)
    parts = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='parts_outword',)
    issued_qty = models.CharField(max_length=150)
    uom = models.ForeignKey(
        Unit, on_delete=models.CASCADE)
    issued_by = models.ForeignKey(
        User, on_delete=models.CASCADE, )
    received_by = models.CharField(max_length=150)
    remarks = models.TextField(blank=True, null=True)
    old_stock = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.id)
    
    def generate_out_ward_sr_no(self):
        self.out_ward_sr_no = "BA0000" + str(self.id)
        self.save()
        return True
    