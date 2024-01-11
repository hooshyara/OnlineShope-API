from rest_framework import serializers
from .models import Products, Comparison, Comment



class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['title','star', 'content', 'cover','active', 'price', 'second_price', 'inventory',  'discouont', 'category', 'percent']
        

class ComparisonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comparison
        fields = ['product', 'user']
        

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['product', 'user', 'star', 'datetime_created', 'datetime_modified',  'text']

 