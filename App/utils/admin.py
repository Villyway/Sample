from django.contrib import admin

from .models import Address
# Register your models here.

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["employee_code", "a_type", "street", "city", "state", "country", "zip"]

    def employee_code(self,obj):
        try:
            return obj.employee_set.all()[-1].employee_code
        except:
            return 0
