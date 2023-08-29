from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.constants.choices import Roles
from .managers import UserManager


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    country_code = models.CharField(max_length=4, default="91")
    role = models.CharField(
        max_length=25, choices=Roles.choices(), default=Roles.OPERATOR.value)
    otp = models.CharField(max_length=4, null=True, blank=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    is_deactivated = models.BooleanField(default=False)
    objects = UserManager()

    def __str__(self):
        return self.name

