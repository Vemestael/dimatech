# Generated by Django 4.0.6 on 2022-08-18 09:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerBillModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_balance_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €'), ('RUB', 'RUB ₽'), ('USD', 'USD $')], default='RUB', editable=False, max_length=3)),
                ('bill_balance', djmoney.models.fields.MoneyField(decimal_places=4, default_currency='RUB', max_digits=19)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Customer Bill',
            },
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €'), ('RUB', 'RUB ₽'), ('USD', 'USD $')], default='RUB', editable=False, max_length=3)),
                ('price', djmoney.models.fields.MoneyField(decimal_places=4, default_currency='RUB', max_digits=19)),
            ],
            options={
                'verbose_name': 'Product',
            },
        ),
        migrations.CreateModel(
            name='TransactionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €'), ('RUB', 'RUB ₽'), ('USD', 'USD $')], default='RUB', editable=False, max_length=3)),
                ('amount', djmoney.models.fields.MoneyField(decimal_places=4, default_currency='RUB', max_digits=19)),
                ('bill_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.customerbillmodel')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Transaction',
            },
        ),
    ]