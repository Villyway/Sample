from django.contrib import admin

# Register your models here.
from .models import Product, Attribute, ProductAttribute, Unit

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["code","umo","stock","minimum_stock_level", "rack_no","tray_no" ]


@admin.register(Attribute)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(ProductAttribute)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["product","attribute","value"]


@admin.register(Unit)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name"]

