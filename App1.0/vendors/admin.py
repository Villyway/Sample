from django.contrib import admin

# Register your models here.
from .models import Vendor, PartyType

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ["code","name","email","gst_no"]


@admin.register(PartyType)
class PartyTypeAdmin(admin.ModelAdmin):
    list_display = ["type"]