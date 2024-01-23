from datetime import date, datetime

from django import forms
from django.core.validators import validate_email

from products.models import (Unit, Product)
from vendors.models import Vendor

