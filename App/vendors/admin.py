from django.contrib import admin

# Register your models here.
from .models import Vendor

@admin.register(Vendor)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["code","name","email","gst_no"]
