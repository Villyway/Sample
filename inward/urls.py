from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (CreateInward, InwardList)

app_name = "inward"

urlpatterns = [
    path("new-inward/", login_required(CreateInward.as_view()), name="new-inward"),
    path("list/", login_required(InwardList.as_view()), name="list"),

]