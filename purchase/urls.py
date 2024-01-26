from django.urls import path
from django.contrib.auth.decorators import login_required

from purchase.views import (MRP, Dashboard, CreatePurchaseOrder)



app_name = "purchase"

urlpatterns = [
    
    path("mrp/",login_required(MRP.as_view()), name="purchase-mrp"),
    path("dashboard/",login_required(Dashboard.as_view()), name="purchase-dashboard"),
    path("create-po/",login_required(CreatePurchaseOrder.as_view()), name="purchase-order"),
    path("<slug:product>/create-po/",login_required(CreatePurchaseOrder.as_view()), name="purchase-order"),
]