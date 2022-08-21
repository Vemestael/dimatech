from Crypto.Hash import SHA1
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from djmoney.money import Money
from djoser import utils
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from config import settings
from main import models, serializers


class UserViewSet(DjoserUserViewSet):
    """
    The class provides base endpoints for User creation and configuration
    """

    def create(self, request, *args, **kwargs):
        """
        Overrides the User create function
        Adding a change of account status to inactive and generating activation link

        Return the activation link
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        user = serializer.instance
        user.is_active = False
        user.save()

        uid = utils.encode_uid(user.pk)
        token = default_token_generator.make_token(user)
        data = {"url": f'http://{request.get_host()}/auth/users/activate/{uid}/{token}'}
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    @action(["get"], detail=False, url_path=r'activate/(?P<uid>[^/.]+)/(?P<token>[^/.]+)')
    def activation(self, request, uid, token):
        """
        Overrides the activation function, changing the endpoint and method from POST to GET

        Returns activation status
        """
        user_data = {'uid': uid, 'token': token}
        serializer = self.get_serializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductAPI(ModelViewSet):
    """
    Rest API for interacting with the Product model

    Has a read-only restriction for unauthorized users
    Provides filtering by the field "price"
    Provides search by the field "title"
    """
    queryset = models.ProductModel.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = {
        'price': ['gte', 'lte'],
    }
    search_fields = ['title']


class CustomerBillAPI(ModelViewSet):
    """
    Rest API for interacting with the CustomerBill model

    Has a read-only restriction for unauthorized users
    Provides filtering by the field "user_id"
    Provides search by the field "username"
    """

    def get_queryset(self):
        """
        Returns for user only with the data associated with him, if he is non admin user
        """
        user = self.request.user
        if user.is_staff:
            return models.CustomerBillModel.objects.all()
        else:
            return models.CustomerBillModel.objects.filter(user_id=user.id)

    serializer_class = serializers.CustomerBillSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user_id']
    search_fields = ['user_id__username']


class TransactionAPI(ModelViewSet):
    """
    Rest API for interacting with the Transaction model

    Has a read-only restriction for unauthorized users
    Provides filtering by "user_id" and "bill_id" fields
    """

    def get_queryset(self):
        """
        Returns for user only with the data associated with him, if he is non admin user
        """
        user = self.request.user
        if user.is_staff:
            return models.TransactionModel.objects.all()
        else:
            return models.TransactionModel.objects.filter(user_id=user.id)

    serializer_class = serializers.TransactionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user_id', 'bill_id']


class PurchaseAPI(ModelViewSet):
    """
    Rest API for interacting with the Purchase model

    Has a read-only restriction for unauthorized users
    Provides filtering by "user_id" and "bill_id" fields
    """

    def get_queryset(self):
        """
        Returns for user only with the data associated with him, if he is non admin user
        """
        user = self.request.user
        if user.is_staff:
            return models.PurchaseModel.objects.all()
        else:
            return models.PurchaseModel.objects.filter(user_id=user.id)

    serializer_class = serializers.PurchaseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user_id', 'bill_id']

    def create(self, request, *args, **kwargs):
        """
        Extends the create function by adding checking and changing bill balance
        """
        bill_obj = models.CustomerBillModel.objects.get(id=request.data['bill_id'])
        product_obj = models.ProductModel.objects.get(id=request.data['product_id'])

        if bill_obj.bill_balance < product_obj.price:
            return Response({'code': status.HTTP_400_BAD_REQUEST, 'message': 'Not enough money to purchase'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            super().create(request, *args, **kwargs)
            bill_obj.bill_balance = bill_obj.bill_balance - product_obj.price
            bill_obj.save()
            return Response(status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(http_method_names=['POST'])
@permission_classes([AllowAny])
def transaction_webhook(request):
    """
    Webhook processes transactions from an external service.
    Checks the integrity of the data by signature, creates a new customer bill if it does not exist.

    Returns the transaction status.
    """
    sign_data = f"{settings.SIGNING_KEY}:{request.POST['transaction_id']}:" \
                f"{request.POST['user_id']}:{request.POST['bill_id']}:{request.POST['amount']}"
    signature = SHA1.new()
    signature.update(sign_data.encode())
    signature = signature.hexdigest()

    if signature != request.POST['signature']:
        return Response(data={'status': status.HTTP_400_BAD_REQUEST, 'message': 'Wrong data'},
                        status=status.HTTP_400_BAD_REQUEST)
    #  create a new customer bill if it does not exist
    user = get_user_model()
    bill_obj = models.CustomerBillModel.objects.get_or_create(id=int(request.POST['bill_id']), defaults={
        'user_id': user.objects.get(id=int(request.POST['user_id']))
    })[0]

    #  Validate transaction data and save them
    serializer = serializers.TransactionSerializer(data=request.POST)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    #  Change bill balance
    amount = Money(amount=request.POST['amount'], currency=bill_obj.bill_balance.currency)
    bill_obj.bill_balance = bill_obj.bill_balance + amount
    bill_obj.save()
    return Response(status=status.HTTP_201_CREATED)
