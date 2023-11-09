from django.db import models

from base.models import Base
from ..constants.choices import AddressType

# Country Manager


class CountryManager(models.Manager):
    def get_queryset(self):
        return super(CountryManager, self).get_queryset()

    def active(self):
        return self.filter(is_active=True)

    def get_country(self, id):
        if self.filter(id=id).exists():
            return self.get(id=id)
        return None

    def get_in(self):
        try:
            return self.get(code="IN")
        except:
            None


# Country Model
class Country(Base):
    name = models.CharField("Country Name", max_length=50, db_index=True)
    code = models.CharField(
        "Country Code", max_length=10, blank=True, null=True)

    objects = CountryManager()

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']

    def __str__(self):
        return self.name


# State Manager
class StateManager(models.Manager):
    def get_queryset(self):
        return super(StateManager, self).get_queryset()

    def active(self):
        return self.filter(is_active=True)

    def get_state(self, id):
        if self.filter(id=id).exists():
            return self.get(id=id)
        return None


# State Model
class State(Base):
    name = models.CharField("State Name", max_length=50, db_index=True)
    code = models.CharField("State Code", max_length=10, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    objects = StateManager()

    class Meta:
        verbose_name_plural = "States"
        ordering = ['name']

    def __str__(self):
        return self.name


# City Manager
class CityManager(models.Manager):
    def get_queryset(self):
        return super(CityManager, self).get_queryset()

    def active(self):
        return self.filter(is_active=True)

    def get_city(self, id):
        if self.filter(id=id).exists():
            return self.get(id=id)
        return None


# City Model
class City(Base):
    name = models.CharField("City Name", max_length=50, db_index=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    objects = CityManager()

    class Meta:
        verbose_name_plural = "Cities"
        ordering = ['name']

    def __str__(self):
        return self.name


class AddressManager(models.Manager):
    def get_queryset(self):
        return super(AddressManager, self).get_queryset()

    def active(self):
        return self.filter(is_active=True)

    def get_address(self, pk):
        if self.filter(id=pk).exists():
            return self.get(id=pk)
        else:
            None


# Address Model
class Address(Base):
    
    street = models.CharField(
        "Address 1", max_length=100, blank=False, null=False)
    street2 = models.CharField(
        "Address 2", max_length=100, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    zip = models.CharField("Zip Code", max_length=100, blank=True, null=True)
    a_type = models.CharField(
        max_length=25, choices=AddressType.choices(), default=AddressType.PERMANENT.value)
    contect_person = models.CharField(max_length=200, blank=True, null=True)
    contect_phone = models.CharField(max_length=20, blank=True, null=True)
    objects = AddressManager()

    def __str__(self):
        return self.street

