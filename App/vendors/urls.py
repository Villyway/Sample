from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (CreateVendor, VendorList, VendorEditView, VendorDelete)

app_name = "vendors"

urlpatterns = [
    path("create/", login_required(CreateVendor.as_view()),
         name="vendor-create"),
    path("list/", login_required(VendorList.as_view()),
         name="vendor-list"),
    path("<slug:id>/edit/", login_required(VendorEditView.as_view()),
         name="vendor-edit"),
    path("<slug:id>/delete/", login_required(VendorDelete.as_view()),
         name="vendor-delete"),
]