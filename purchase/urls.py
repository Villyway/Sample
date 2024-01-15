from django.urls import path
from django.contrib.auth.decorators import login_required

from purchase.views import (MRP, Dashboard)



app_name = "purchase"

urlpatterns = [
    
    path("mrp/",login_required(MRP.as_view()), name="purchase-mrp"),
    path("dashboard/",login_required(Dashboard.as_view()), name="purchase-dashboard"),
]