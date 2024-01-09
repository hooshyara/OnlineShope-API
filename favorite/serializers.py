from rest_framework import serializers
from .models import Favorite
from products.serializers import ProductSerializers
from accounts.serializers import UserSerializers


class FavoriteSerializers(serializers.ModelSerializer):
    user =UserSerializers(read_only=True)
    product = ProductSerializers(read_only=True)
    class Meta:
        model = Favorite
        fields = ['user', 'product']
        

