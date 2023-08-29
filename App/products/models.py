from django.db import models

from base.models import Base
from vendors.models import Vendor
from users.models import User

# Create your models here.
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

    def __str__(self):
        return self.code


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

    # objects = AttributeManager()

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

    def __str__(self):
        return self.id
    

#OutWord
class Outword(Base):
    out_ward_sr_no = models.CharField(max_length=20, unique=True)
    parts = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='parts_outword',)
    issued_qty = models.CharField(max_length=150)
    uom = models.ForeignKey(
        Unit, on_delete=models.CASCADE)
    issued_by = models.ForeignKey(
        User, on_delete=models.CASCADE, )
    received_by = models.CharField(max_length=150)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.out_word_sr_no
    