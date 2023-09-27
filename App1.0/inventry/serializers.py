from rest_framework import serializers

from .models import InWord

class InwordOfBillWiseProductSerializer(serializers.ModelSerializer):
    
    product = serializers.SerializerMethodField()

    class Meta:
        model = InWord
        fields = ["product"]

    def get_product(self,obj):
        product = []
        for i in obj:
            product.append({"code":i.part.code,"name":i.part.name,"received_qty":i.received_qty,"qc":i.qc_status})
        return product
    
    
        