from django.db import models

from base.models import Base
from utils.constants.choices import CustomerType
from utils.models import Address

# Create your models here.

class Customer(Base):
    code = models.CharField(max_length=30, unique=True, blank=True, null=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    mobile = models.CharField(max_length=50, null=True, blank=True)
    country_code = models.CharField(max_length=4, default="91")
    email = models.EmailField(null=True, blank=True)
    gst_no = models.CharField(max_length=16, blank=True, null=True)
    type = models.CharField(
        max_length=25, choices=CustomerType.choices(), default=CustomerType.value)
    address = models.ManyToManyField(Address, blank=True)
    is_user = models.BooleanField(default=False)
    

    def __str__(self):
        return self.code

