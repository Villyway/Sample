from import_export import resources
from .models import Product

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ("part_no","name","code","category__name","quality_type__name")
        export_order = ("part_no","name","code","category__name","quality_type__name")