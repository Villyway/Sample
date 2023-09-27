from rest_framework import serializers

from .models import Vendor

class VendorDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = ["code","name","gst_no"]
    