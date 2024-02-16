from django.urls import path
from django.contrib.auth.decorators import login_required

from purchase.views import (MRP, Dashboard, CreatePurchaseOrder, 
                            OrderAgainstMRP, PoList, SingelPurchaseOrder, ExportPO, DeletePoProduct,GetPO)



app_name = "purchase"

urlpatterns = [
    
    path("mrp/",login_required(MRP.as_view()), name="purchase-mrp"),
    path("order-mrp/",login_required(OrderAgainstMRP.as_view()), name="purchase-order-mrp"),
    path("dashboard/",login_required(Dashboard.as_view()), name="purchase-dashboard"),
    path("create-po/",login_required(CreatePurchaseOrder.as_view()), name="purchase-order"),
    path("list/",login_required(PoList.as_view()), name="purchase-order-list"),
    path("<slug:product>/create-po/",login_required(CreatePurchaseOrder.as_view()), name="purchase-order"),
    path("<slug:id>/po/",login_required(SingelPurchaseOrder.as_view()), name="purchase-singel-order"),
    path("<slug:id>/remove-product/",login_required(DeletePoProduct.as_view()), name="remove-product-of-po"),
    path("export/<slug:id>/po/",login_required(ExportPO.as_view()), name="export-purchase-singel-order"),
    path("<slug:pk>/",login_required(GetPO.as_view()), name="get-po"),

    
]