from rest_framework import serializers
from .models import User, UserAddress


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password','groups','user_permissions')

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['id','pincode', 'full_address', "lat", "lng"]

class UserAddressRetrunSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = '__all__'
