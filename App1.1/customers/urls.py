from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
                     Dashboard, CreateCustomer, SingleCustomerAndAddAddress,
                     EditCustomer
                    )

app_name = "customers"

urlpatterns = [
    path("dashboard",login_required(Dashboard.as_view()), name="dashboard"),
    path("create-customer",login_required(CreateCustomer.as_view()), name="create-customer"),
    path("<slug:id>/show",login_required(SingleCustomerAndAddAddress.as_view()), name="show-customer"),
    path("<slug:id>/edit",login_required(EditCustomer.as_view()), name="edit-customer"),

]