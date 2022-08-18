import requests
from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend
from djoser import utils
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
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


class UserViewSet(DjoserUserViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        user = serializer.instance
        user.is_active = False
        user.save()

        uid = utils.encode_uid(user.pk)
        token = default_token_generator.make_token(user)
        data = {
            "url": f'http://{request.get_host()}/auth/activate/{uid}/{token}'
        }
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class UserActivationView(APIView):
    def get(self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/auth/users/activation/"
        post_data = {'uid': uid, 'token': token}
        response = requests.post(post_url, data=post_data)
        content = response.text
        if response.status_code == status.HTTP_204_NO_CONTENT and not content:
            content = "User is successfully activated"
        return Response(content)
