from rest_framework import serializers
from .models import Cart, Order, OrderItem
from products.serializers import ProductSerializers
from accounts.serializers import UserSerializers



class CartSerializers(serializers.ModelSerializer):
    user =UserSerializers(read_only=True)
    product = ProductSerializers(read_only=True)
    class Meta:
        model = Cart
        fields = ['user', 'product', 'end_price', 'count']
        

class OrderSerializers(serializers.ModelSerializer):
    user =UserSerializers(read_only=True)
    class Meta:
        model = Order
        fields = ['user', 'first_name', 'last_name', 'city', 'address', 'post_id', 'description', ]
        

class OrderItemSerializers(serializers.ModelSerializer):
    user =UserSerializers(read_only=True)
    product = ProductSerializers(read_only=True)
    order = OrderSerializers(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['user', 'product', 'order']
        

