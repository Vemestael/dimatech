from django.conf import settings
from django.db import models

from djmoney.models.fields import MoneyField


class ProductModel(models.Model):
    """
    Consists of:
    title: CharField
    description: TextField
    price: MoneyField
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = MoneyField(max_digits=19, decimal_places=4, default_currency='RUB', default=0.0)

    class Meta:
        verbose_name = 'Product'

    def __str__(self):
        return f'{self.title} | {self.price}'


class CustomerBillModel(models.Model):
    """
    Consists of:
    user_id: ForeignKey to User
    bill_balance: MoneyField
    """
    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bill_balance = MoneyField(max_digits=19, decimal_places=4, default_currency='RUB', default=0.0)

    class Meta:
        verbose_name = 'Customer Bill'

    def __str__(self):
        return f'{self.id}'


class TransactionModel(models.Model):
    """
    Consists of:
    user_id: ForeignKey to User
    bill_id: ForeignKey to CustomerBillModel
    amount: MoneyField
    """
    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bill_id = models.ForeignKey(to=CustomerBillModel, on_delete=models.CASCADE)
    amount = MoneyField(max_digits=19, decimal_places=4, default_currency='RUB', default=0.0)

    class Meta:
        verbose_name = 'Transaction'

    def __str__(self):
        return f'{self.bill_id} | {self.amount}'


class PurchaseModel(models.Model):
    """
    Consists of:
    product_id: ForeignKey to ProductModel
    user_id: ForeignKey to User
    bill_id: ForeignKey to CustomerBillModel
    """
    product_id = models.ForeignKey(to=ProductModel, on_delete=models.CASCADE)
    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bill_id = models.ForeignKey(to=CustomerBillModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Purchase'

    def __str__(self):
        return f'{self.product_id} | {self.user_id}'
