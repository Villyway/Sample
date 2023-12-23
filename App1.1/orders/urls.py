from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
                     Dashboard, CreateOrders, OrderList,
                     SingelOrderView, ChangeDispatchStatusOfOrderOfChild,
                     ChangeDeliveryStatus, OrderDispatchProcess, ExportDispatchNote, AddLRNo,
                     ChangeOrderConfirmationStatus, OrderOfProductCancleation, ExportData, OrdersReport, OrdersCustomReportResponse,
                     OrderSearch
                    )

app_name = "orders"

urlpatterns = [
    path("dashboard",login_required(Dashboard.as_view()), name="orders-dashboard"),
    path("<slug:id>/create-orders",login_required(CreateOrders.as_view()), name="orders-create"),
    path("orders-list",login_required(OrderList.as_view()), name="orders-list"),
    path("<slug:id>/order-details",login_required(SingelOrderView.as_view()), name="order-details"),
    path("<slug:id>/change-dispatch-status/",login_required(ChangeDispatchStatusOfOrderOfChild.as_view()), name="change-order-dispatch-status"),
    path("<slug:id>/change-delivery-status/",login_required(ChangeDeliveryStatus.as_view()), name="change-order-delivery-status"),
    path("<slug:id>/order-dispatch-process",login_required(OrderDispatchProcess.as_view()), name="order-dispatch-process"),
    path("<slug:id>/order-dispatch-note",login_required(ExportDispatchNote.as_view()), name="order-dispatch-note"),
    path("pending-lr-details", login_required(AddLRNo.as_view()), name='pending-lr-details'),
    path("<slug:id>/change-order-confirmation", login_required(ChangeOrderConfirmationStatus.as_view()), name='change-order-confirmation'),
    path("<slug:id>/order-of-item-cancle", login_required(OrderOfProductCancleation.as_view()), name='order-item-cancle'),
    path("export-report/", login_required(ExportData.as_view()), name='export-report'),
    path("report/", login_required(OrdersReport.as_view()), name='orders-report'),
    path("search-report/", login_required(OrdersCustomReportResponse.as_view()), name='search-report'),
    path("search/", login_required(OrderSearch.as_view()), name='search-orders'),

    
]