from rest_framework import serializers
from .models import Products



class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['title','star', 'content', 'cover','active', 'price', 'second_price', 'inventory',  'discouont', 'category']
        

