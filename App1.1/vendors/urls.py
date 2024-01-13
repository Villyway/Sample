from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (CreateVendor, VendorList, VendorEditView,
                    VendorDelete, Dashboard, GetVenderName,
                    CreateCategories, RemoveVendorCategory, VendorDetails,
                    SearchVendor,
                    )

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
    path("dashboard",login_required(Dashboard.as_view()), name="vendor-dashboard"),
    path("<slug:id>/get-vendor-name",login_required(GetVenderName.as_view()), name="vendor-get-name"),
    path("vendor-category",
         login_required(CreateCategories.as_view()), name="vendor-category"),
    path("remove-category/", login_required(RemoveVendorCategory.as_view()),
         name="remove-category"),
    path("<slug:id>/vendor-details/", login_required(VendorDetails.as_view()), name="vendor-details"),
    path("search/", login_required(SearchVendor.as_view()),
         name="product-search"),
]