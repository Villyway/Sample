from collections import defaultdict

from django.core.management.base import BaseCommand
from django.conf import settings

from products.models import Product, BOMItem
from orders.models import OrderOfProduct




class Command(BaseCommand):
    help = """Generate MOQ"""

    def calculate_mrp(self, product, quantity, mrp_dict=None):
        if mrp_dict is None:
            mrp_dict = defaultdict(int)

        bom_items = BOMItem.objects.filter(product=product)

        for bom_item in bom_items:
            raw_material = bom_item.component
            component_quantity = bom_item.quantity * quantity

            # Aggregate the quantity for the same raw material
            mrp_dict[raw_material] += component_quantity

            # Recursively calculate MRP for the raw material
            self.calculate_mrp(raw_material, component_quantity, mrp_dict)
        return mrp_dict

    def aggregate_mrp(self, mrp_results):

        # print()
        aggregated_mrp = defaultdict(int)

        for mrp_result in mrp_results:
            for product, quantity in mrp_result.items():
                aggregated_mrp[product] += quantity

        return aggregated_mrp

    def generate(self):
        product_objs = []
        products = OrderOfProduct.objects.product_wise_average_orders()
        
        for i in products:
            product_objs.append(self.calculate_mrp(Product.objects.by_code(i['product__code']),int(i['avg_order_qty'])))

        results = self.aggregate_mrp(product_objs)
        
        for i, j in dict(results).items():
            i.minimum_stock_level = j
            i.save()
        
        print("all Saved, Please Check!!")
            # __p = {}
            # __p['id'] = i.id
            # __p['qty'] = j
            
            

        

        

    def handle(self, *args, **kwargs):
        self.generate()
