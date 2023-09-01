from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (ProductList, CreateProduct, 
                    ProductEditView, ProductProperty, 
                    RemoveProductProperty, InwardCreateView,
                    OutwardCreateView)

app_name = "products"

urlpatterns = [
    path("list",login_required(ProductList.as_view()), name="products-list"),
    path("create",login_required(CreateProduct.as_view()), name="products-create"),
    path("<slug:id>/edit",login_required(ProductEditView.as_view()), name="products-edit"),
    path("<int:id>/product-property/",
         login_required(ProductProperty.as_view()), name="product-property"),
    path("remove-property/", login_required(RemoveProductProperty.as_view()),
         name="remove-property"),
    path("inward/", login_required(InwardCreateView.as_view()),
         name="inward"),
    path("outward/", login_required(OutwardCreateView.as_view()),
         name="outward"),

]