from django.contrib import admin

# Register your models here.

from orders.models import OrderDetails, OrderOfProduct

@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ["customer","order_no", "date", "order_status", "remarks"]


@admin.register(OrderOfProduct)
class OrderOfProductAdmin(admin.ModelAdmin):
    list_display = ["order","product", "order_qty", "packing_type", "status"]