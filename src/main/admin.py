from django.contrib import admin

import main.models as models


@admin.register(models.ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'price')


@admin.register(models.CustomerBillModel)
class CustomerBillAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'bill_balance')


@admin.register(models.TransactionModel)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'bill_id', 'amount')
