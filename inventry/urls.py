from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
                    Dashboard, ExportData, 
                    SimpleAddStock, StockHistoryInJson, StockHistoriesList, 
                    InventryReport, InventryReportStock)

app_name = "inventry"

urlpatterns = [
    path("dashboard",login_required(Dashboard.as_view()), name="inventry-dashboard"),
    path("add-stock/", login_required(SimpleAddStock.as_view()), name="add-stock"),
    path("<slug:id>/stock-history/", login_required(StockHistoryInJson.as_view()), name="json-stock-history"),
    path("stock-history/", login_required(StockHistoriesList.as_view()), name="stock-histories"),
    path("reports/", login_required(InventryReport.as_view()), name="stock-report"),
    path("export-report/",login_required(ExportData.as_view()), name="export-today"),
    path("search-report/",login_required(InventryReportStock.as_view()), name="search-report"),

]