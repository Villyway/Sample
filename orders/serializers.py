from datetime import datetime

from django.db import transaction
from rest_framework import serializers

from orders.models import OrderDetails, OrderOfProduct
from products.models import Product
from utils.constants import PackingType
from customers.models import Customer
from utils.views import generate_order_dispatch_no





class OrderOfProductCreateSerializer(serializers.Serializer):

    part_no = serializers.ListField(child=serializers.CharField())
    qty = serializers.ListField(child=serializers.IntegerField())
    order_no = serializers.CharField(max_length=80)
    remarks = serializers.CharField(max_length=5000)
    
    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        customer = Customer.objects.get(user=user)
        with transaction.atomic():
            order = OrderDetails()
            order.customer = customer
            order.date = datetime.today().date()
            order.remarks = validated_data['remarks']
            order.created_by = request.user.id
            order.billing_add = customer.address.first()
            order.shipped_add = customer.address.first()
            order.sales_challan = validated_data['order_no']
            order.save()
            order.order_no = generate_order_dispatch_no(order.id)
            order.save()

            for product_name, quantity_value in zip(validated_data['part_no'],validated_data['qty']):
                if Product.objects.by_code(product_name):
                    product = Product.objects.by_code(product_name)
                    order_of_product = OrderOfProduct()
                    order_of_product.order = order
                    order_of_product.product = product
                    order_of_product.order_qty = quantity_value
                    order_of_product.uom = product.umo
                    order_of_product.packing_type = PackingType.BOX.value
                    order_of_product.created_by = request.user.id
                    order_of_product.transport_compny = 'DHL'
                    order_of_product.save()
        return {"message":"success", "status":True, "order_no":order.order_no}
        


    


    
