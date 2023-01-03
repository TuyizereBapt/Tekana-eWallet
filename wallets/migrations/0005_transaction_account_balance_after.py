# Generated by Django 4.1.4 on 2023-01-03 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0004_rename_available_account_balance_transaction_account_balance_before'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='account_balance_after',
            field=models.FloatField(null=True, verbose_name="Account's balance after the transaction"),
        ),
    ]
