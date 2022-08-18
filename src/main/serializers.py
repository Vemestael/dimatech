from rest_framework.serializers import HyperlinkedModelSerializer

import main.models as models


class ProductSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.ProductModel
        fields = '__all__'


class CustomerBillSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.CustomerBillModel
        fields = '__all__'


class TransactionSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = models.TransactionModel
        fields = '__all__'
