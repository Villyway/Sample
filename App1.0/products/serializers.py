from rest_framework import serializers

from .models import Product

class InwordOfProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ["code","name"]

    