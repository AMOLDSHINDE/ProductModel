from rest_framework import serializers
from .models import ProductModel

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ["id", "name", "price", "retailer_name"]

        
