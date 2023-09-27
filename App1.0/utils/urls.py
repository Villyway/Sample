from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (CityView,
                    StateView)


app_name = "utils"

urlpatterns = [
    path("<int:id>/city_ajex/", CityView.as_view(),
         name="city"),
    path("<int:id>/state_ajex/", StateView.as_view(),
         name="state"),

    # list of country, state, city:
    # path("country/", CountryAPIView.as_view(), name="country-list"),
    # path("state/<int:pk>/", StateAPIView.as_view(), name="state-list"),
    # path("city/<int:pk>/", CityAPIView.as_view(), name="city-list"),

]
