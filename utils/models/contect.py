from django.db import models

from base.models import Base
from utils.constants import Department

# Country Model
class ContectMail(Base):
    email = models.EmailField(null=True, blank=True)
    department = models.CharField(
        max_length=25, choices=Department.choices(), default=Department.INFO.value)
    password = models.CharField(max_length=200, null=True, blank=True)

    
    
    

    