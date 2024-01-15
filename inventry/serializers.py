from rest_framework import serializers

from .models import InWord, SimpleStockUpdte

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
    
    
class StockHistorySerializer(serializers.ModelSerializer):
    
    histories = serializers.SerializerMethodField()


    class Meta:
        model = SimpleStockUpdte
        fields = ["histories"]

    def get_histories(self,obj):
        product = []
        for i in obj:
            product.append({"part_no":i.part.part_no,"old_stock":i.old_stock,"date_time":i.created_at,"received_qty":i.received_qty,"ava_stock":i.quantity_on_hand,"trans_type":i.transection_type,"received_by":i.received_by})
        return product
        


