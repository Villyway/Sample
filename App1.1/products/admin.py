from django.contrib import admin
from import_export.admin import ExportActionMixin

# Register your models here.
from .models import Product, Attribute, ProductAttribute, Unit

@admin.register(Product)
class ProductAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ["code","umo","stock","minimum_stock_level", "rack_no","tray_no" ]


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(ProductAttribute)
class ProductAttributeAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display = ["product","attribute","value"]


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ["name"]



