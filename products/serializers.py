from rest_framework import serializers
from .models import Products, Comparison



class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['title','star', 'content', 'cover','active', 'price', 'second_price', 'inventory',  'discouont', 'category']
        

class ComparisonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comparison
        fields = ['product', 'user']
        

