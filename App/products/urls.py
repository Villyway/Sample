from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (ProductList, CreateProduct, 
                    ProductEditView, ProductProperty, 
                    RemoveProductProperty, 
                    )

app_name = "products"

urlpatterns = [
    path("list",login_required(ProductList.as_view()), name="products-list"),
    path("create",login_required(CreateProduct.as_view()), name="products-create"),
    path("<slug:id>/edit",login_required(ProductEditView.as_view()), name="products-edit"),
    path("<int:id>/product-property/",
         login_required(ProductProperty.as_view()), name="product-property"),
    path("remove-property/", login_required(RemoveProductProperty.as_view()),
         name="remove-property"),
    

]