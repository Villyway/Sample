from django.contrib import admin

# Register your models here.
from .models import Product, Attribute, ProductAttribute, Unit, InWord, Outword

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["code","umo","stock","minimum_stock_level", "rack_no","tray_no" ]


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ["product","attribute","value"]


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Outword)
class OutwordAdmin(admin.ModelAdmin):
    list_display = ["out_ward_sr_no","parts", "issued_qty", "issued_by", "received_by"]


@admin.register(InWord)
class InWordAdmin(admin.ModelAdmin):
    list_display = ["grn_no","bill_no","bill_date","part","qc_status"]

