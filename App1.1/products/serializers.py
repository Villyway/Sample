from rest_framework import serializers

from .models import Product

class InwordOfProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ["code","name"]

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["code", "part_no", "name", "image","category","description"]


class ProductSerializerWithId(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id","code", "part_no", "name", "image","category","description"]

