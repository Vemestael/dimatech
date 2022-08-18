from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from main import models, serializers


class ProductAPI(ModelViewSet):
    queryset = models.ProductModel.objects.all()
    serializer_class = serializers.ProductSerializer
    filterset_fields = {
        'price': ['gte', 'lte'],
    }


class CustomerBillAPI(ModelViewSet):
    queryset = models.CustomerBillModel.objects.all()
    serializer_class = serializers.CustomerBillSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user_id']
    search_fields = ['user_id__username']


class TransactionAPI(ModelViewSet):
    queryset = models.TransactionModel.objects.all()
    serializer_class = serializers.TransactionSerializer
