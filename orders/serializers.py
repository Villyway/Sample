from rest_framework import serializers

from orders.models import OrderDetails, OrderOfProduct
from customers.models import Customer


class OrderOfProductCreateSerializer(serializers.Serializer):

    part_no = serializers.ListField(child=serializers.CharField())
    qty = serializers.ListField(child=serializers.IntegerField())
    order_no = serializers.CharField(max_length=80)
    billing_address = serializers.CharField(max_length=500)
    shipping_address = serializers.CharField(max_length=500)

    def create(self, validated_data):
        request = self.context.get("request")
        return {}
        


    


    
