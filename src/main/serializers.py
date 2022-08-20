from djoser.serializers import User
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault

import main.models as models


class UserSerializer(DjoserUserSerializer):
    """
    User model serializer

    Overrides the fields used
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active']
        read_only_fields = ['id', 'username']


class ProductSerializer(ModelSerializer):
    """
    Product model serializer
    """
    class Meta:
        model = models.ProductModel
        fields = '__all__'


class CustomerBillSerializer(ModelSerializer):
    """
    Customer Bill model serializer

    user_id is defined as the current user
    """
    user_id = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = models.CustomerBillModel
        fields = '__all__'


class TransactionSerializer(ModelSerializer):
    """
    Customer Bill model serializer

    user_id is defined as a list of existing users
    """
    user_id = PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = models.TransactionModel
        fields = '__all__'


class PurchaseSerializer(ModelSerializer):
    """
    Customer Bill model serializer

    user_id is defined as the current user
    """
    user_id = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = models.PurchaseModel
        fields = '__all__'
