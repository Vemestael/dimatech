from django.contrib.auth.models import User
from django.db import models

from djmoney.models.fields import MoneyField


class ProductModel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = MoneyField(max_digits=19, decimal_places=4, default_currency='RUB')

    class Meta:
        verbose_name = 'Product'

    def __str__(self):
        return f'{self.title} | {self.price}'


class CustomerBillModel(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    bill_balance = MoneyField(max_digits=19, decimal_places=4, default_currency='RUB')

    class Meta:
        verbose_name = 'Customer Bill'

    def __str__(self):
        return f'{self.id}'


class TransactionModel(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    bill_id = models.ForeignKey(to=CustomerBillModel, on_delete=models.CASCADE)
    amount = MoneyField(max_digits=19, decimal_places=4, default_currency='RUB')

    class Meta:
        verbose_name = 'Transaction'

    def __str__(self):
        return f'{self.bill_id} | {self.amount}'