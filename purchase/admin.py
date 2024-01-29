from django.contrib import admin

# Register your models here.
from purchase.models import (TaxCode, PaymentTerms, TermsAndConditions,
                             PurchaseOrder, PurchaseItem,)


@admin.register(TaxCode)
class TaxCodeAdmin(admin.ModelAdmin):
    list_display = ['name','code', 'value']
    search_fields = ['code','name','value']


@admin.register(PaymentTerms)
class PaymentTermsAdmin(admin.ModelAdmin):
    list_display = ['name','description']
    search_fields = ['name']


@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ['name','description']
    search_fields = ['name']


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['po_no', 'vendor','status','del_date','close_date']
    search_fields = ['po_no','vendor__comany_name']


@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ['po','part','qty','del_status']
    search_fields = ['po','part','po__vendor__comany_name']
