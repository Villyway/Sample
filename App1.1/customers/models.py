from django.db import models

from base.models import Base
from utils.models import Address

# Create your models here.
class Customer(Base):
    name = models.CharField(max_length=150, null=True, blank=True)
    mobile = models.CharField(max_length=50, null=True, blank=True)
    country_code = models.CharField(max_length=4, default="91")
    email = models.EmailField(null=True, blank=True)
    contect_person = models.CharField(max_length=150, null=True, blank=True)
    address = models.ManyToManyField(Address, blank=True)
    mobile1 = models.CharField(max_length=50, null=True, blank=True)
    gst_no = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name