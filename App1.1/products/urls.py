from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (ProductList, CreateProduct, 
                    ProductEditView, ProductProperty, 
                    RemoveProductProperty, Dashboard,
                    RemoveProductCategory, CreateCategories,
                    GetProductName, CreateQuality, BomItemList,
                    SingelBom, CategoryWiseList, ExportData, CreatBOM, SingleProduct, SingleProductByPartNo, ProductSearch,
                    AddVendorOfProduct
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
    path("product-quality/", login_required(CreateQuality.as_view()),
         name="product-quality"),
    path("bom-list/", login_required(BomItemList.as_view()),
         name="bom-list"),
    path("<slug:id>/bom", login_required(SingelBom.as_view()),
         name="product-bom"),
    path("<slug:id>/list-product", login_required(CategoryWiseList.as_view()),
         name="category-product"),
    path("product-export",login_required(ExportData.as_view()), name="product-export"),
    path("create-bom/",login_required(CreatBOM.as_view()), name="bom-create"),
    path("<slug:id>/single-product", login_required(SingleProduct.as_view()),
         name="single-product"),
    path("<slug:id>/single-product-part-no", login_required(SingleProductByPartNo.as_view()),
         name="single-product-part-no"),
    path("search/", login_required(ProductSearch.as_view()),
         name="product-search"),

    path("<slug:id>/add-vendor", login_required(AddVendorOfProduct.as_view()), name="add-vendor-of-product"),
]