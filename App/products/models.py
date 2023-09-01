from django.db import models
from django.core.files.storage import default_storage

from base.models import Base
from vendors.models import Vendor
from users.models import User
from .managers import ProductManager, AttributeManager


#upload file
def upload_file(instance, filename, dir_name):
    name = filename.name.replace(" ", "_")
    url = "%s/%d/%s" % (dir_name,int(instance.id), name)
    file_name = default_storage.save(url, filename)
    return file_name


# Unit
class Unit(Base):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

#Product
class Product(Base):
    code = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    umo = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name='product_unit',)
    specification = models.TextField(blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True, default=0)
    minimum_stock_level = models.IntegerField(blank=True, null=True, default=0)
    rack_no = models.IntegerField(blank=True, null=True, default=0)
    tray_no = models.IntegerField(blank=True, null=True, default=0)
    image = models.URLField(max_length=500, blank=True, null=True)

    objects = ProductManager()

    def __str__(self):
        return self.code
    
    def save_image_url(self, image, file_url):
        image = upload_file(self, image,"products/"+ self.code)
        image = file_url + '/media/' + image
        self.image = image
        self.save()
        return True


# Model for Attribute
class Attribute(Base):
    name = models.CharField("Name", max_length=50)

    def __str__(self):
        return self.name


# Model for Property
class ProductAttribute(Base):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_property',)
    attribute = models.ForeignKey(
        Attribute, on_delete=models.SET_NULL, null=True, related_name='property_attribute')
    value = models.CharField(max_length=150)

    objects = AttributeManager()

    def __str__(self):
        return self.attribute.name


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
        file_obj = upload_file(self, file_obj,"inward/"+ self.vendor.code)
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
    