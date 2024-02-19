from django.contrib import admin

from inward.models import Inward, InwardItems

# Register your models here.
@admin.register(Inward)
class InwardAdmin(admin.ModelAdmin):
    list_display = ['inward_no']

@admin.register(InwardItems)
class InwardItemsAdmin(admin.ModelAdmin):
    list_display = ['inward','received_item','qty']
