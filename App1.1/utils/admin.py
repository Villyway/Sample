from django.contrib import admin

from .models import Address, State, City, Country
# Register your models here.

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["a_type", "street", "city", "state", "country", "zip"]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["name"]


    