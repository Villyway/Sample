from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
                     Dashboard, CreateOrders,
                     
                    )

app_name = "orders"

urlpatterns = [
    path("dashboard",login_required(Dashboard.as_view()), name="orders-dashboard"),
    path("create-orders",login_required(CreateOrders.as_view()), name="orders-create"),
]