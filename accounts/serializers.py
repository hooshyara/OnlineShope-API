from rest_framework import serializers
from .models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mobile', 'last_name', 'first_name', 'born_dateTime', 'post_id',
                  'national_id', 'address', 'city', 'province', 'gender', 'profile_picture']
