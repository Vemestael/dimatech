from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework.serializers import HyperlinkedModelSerializer

import main.models as models

User = get_user_model()


class UserSerializer(DjoserUserSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active']
        read_only_fields = ['id', 'username']


class ProductSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.ProductModel
        fields = '__all__'


class CustomerBillSerializer(HyperlinkedModelSerializer):
    user_id = UserSerializer()

    class Meta:
        model = models.CustomerBillModel
        fields = '__all__'


class TransactionSerializer(HyperlinkedModelSerializer):
    user_id = UserSerializer()

    class Meta:
        model = models.TransactionModel
        fields = '__all__'
