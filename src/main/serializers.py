from djoser.serializers import User
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault

import main.models as models


class UserSerializer(DjoserUserSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active']
        read_only_fields = ['id', 'username']


class ProductSerializer(ModelSerializer):
    class Meta:
        model = models.ProductModel
        fields = '__all__'


class CustomerBillSerializer(ModelSerializer):
    user_id = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = models.CustomerBillModel
        fields = '__all__'


class TransactionSerializer(ModelSerializer):
    user_id = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = models.TransactionModel
        fields = '__all__'


class PurchaseSerializer(ModelSerializer):
    user_id = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = models.PurchaseModel
        fields = '__all__'
