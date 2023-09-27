from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (ProductList, CreateProduct, 
                    ProductEditView, ProductProperty, 
                    RemoveProductProperty, Dashboard,
                    RemoveProductCategory, CreateCategories,
                    GetProductName
                    )

app_name = "products"

urlpatterns = [
    path("list",login_required(ProductList.as_view()), name="products-list"),
    path("dashboard",login_required(Dashboard.as_view()), name="products-dashboard"),
    path("create",login_required(CreateProduct.as_view()), name="products-create"),
    path("<slug:id>/edit",login_required(ProductEditView.as_view()), name="products-edit"),
    path("<slug:id>/product-name",login_required(GetProductName.as_view()), name="products-name"),
    path("<int:id>/product-property/",
         login_required(ProductProperty.as_view()), name="product-property"),
    path("remove-property/", login_required(RemoveProductProperty.as_view()),
         name="remove-property"),
    path("product-category",
         login_required(CreateCategories.as_view()), name="product-category"),
    path("remove-category/", login_required(RemoveProductCategory.as_view()),
         name="remove-category"),
    

]