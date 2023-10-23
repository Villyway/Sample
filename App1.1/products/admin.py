from django.contrib import admin
from import_export.admin import ExportActionMixin

# Register your models here.
from .models import Product, Attribute, ProductAttribute, Unit, PartQuality, BOMItem, Categories

@admin.register(Product)
class ProductAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ["code","umo","stock","minimum_stock_level", "rack_no","tray_no" ]
    search_fields = ['part_no','name','code']


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(ProductAttribute)
class ProductAttributeAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display = ["product","attribute","value"]


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(PartQuality)
class PartQualityAdmin(admin.ModelAdmin):
    list_display= ["code","name"]

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display= ["name"]


@admin.register(BOMItem)
class BOMItemAdmin(admin.ModelAdmin):
    list = ["product__name"]
    search_fields = ['product__code']