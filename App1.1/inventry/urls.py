from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (InwardCreateView,
                    OutwardCreateView, Dashboard, GetBillNoByInword, QCView, SimpleAddStock)

app_name = "inventry"

urlpatterns = [
    path("inward/", login_required(InwardCreateView.as_view()),
         name="inward"),
    path("outward/", login_required(OutwardCreateView.as_view()),
         name="outward"),
    path("dashboard",login_required(Dashboard.as_view()), name="inventry-dashboard"),
    path("<slug:id>/bill-inword",login_required(GetBillNoByInword.as_view()), name="bill-inword"),
    path("qc-list/",login_required(QCView.as_view()), name="qc-list"),
    path("add-stock/", login_required(SimpleAddStock.as_view()), name="add-stock")

]