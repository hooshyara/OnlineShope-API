from rest_framework import serializers
from .models import Cart
from products.serializers import ProductSerializers
from accounts.serializers import UserSerializers



class CartSerializers(serializers.ModelSerializer):
    user =UserSerializers(read_only=True)
    product = ProductSerializers(read_only=True)
    class Meta:
        model = Cart
        fields = ['user', 'product', 'end_price', 'count']
        

