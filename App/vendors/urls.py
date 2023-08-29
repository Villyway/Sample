from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (CreateVendor)

app_name = "vendors"

urlpatterns = [
    path("create/", login_required(CreateVendor.as_view()),
         name="vendor-create"),
]