from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

from customers.models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'contect_person','mobile','email']

# class customer_entryAdmin(ImportExportModelAdmin):   # FOR ADMIN IMPORT EXPORT ONLY 
#     pass


# admin.site.register(Customer, customer_entryAdmin)   
# class Customersresource(resources.ModelResource):
        
#         class Meta:
#             model = Customer
            