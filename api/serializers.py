from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError

from authentication.models import CustomUser
from product.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Hash the password before saving the user
        validated_data['password'] = make_password(validated_data.get('password'))
        user = super(UserSerializer, self).create(validated_data)
        return user

    def update(self, instance, validated_data):
        # Hash the password before updating the user
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).update(instance, validated_data)


###################################################### Serializer Verify ###############################################
def custom_code_validator(value):
    if not value.isdigit() or len(value) != 6:
        raise ValidationError('Invalid verification code. It must be a 6-digit number.')


class VerifySerializer(serializers.ModelSerializer):
    code = serializers.CharField(
        max_length=6,
        required=True,
        help_text='Enter the 6-digit verification code',
        error_messages={
            'blank': 'Verification code cannot be blank',
            'max_length': 'Verification code must be exactly 6 characters long',
            'min_length': 'Verification code must be exactly 6 characters long',
        },
        validators=[custom_code_validator]
    )

    class Meta:
        model = CustomUser
        fields = ['code']

    ###################################################### End Serializer Verify ###############################################


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


# end of user


# start Color
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color_product
        fields = "__all__"


# start Size
class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size_product
        fields = "__all__"


# start Product
class ProductSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(many=True)
    sizes = SizeSerializer(many=True)

    class Meta:
        model = Products_shop
        fields = "__all__"


# start Cart Item
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"


# start Order
class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"


# start Invoice
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"


