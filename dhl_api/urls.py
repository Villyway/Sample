from django.urls import path


from dhl_api.views import TrackAllCheckPoints

app_name = "dhl_api"

urlpatterns = [

    path('<slug:order_no>/track-order/', TrackAllCheckPoints.as_view(), name="track-order"),
]