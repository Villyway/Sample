from django.contrib import admin

from .models import Outword, InWord, SimpleStockUpdte

# Register your models here.
@admin.register(Outword)
class OutwordAdmin(admin.ModelAdmin):
    list_display = ["out_ward_sr_no","parts", "issued_qty", "issued_by", "received_by"]


@admin.register(InWord)
class InWordAdmin(admin.ModelAdmin):
    list_display = ["grn_no","bill_no","bill_date","part","qc_status"]

@admin.register(SimpleStockUpdte)
class SimpleStockUpdteAdmin(admin.ModelAdmin):
    list_display = ["part","created_at", "old_stock","transection_type", "received_qty","quantity_on_hand"]
