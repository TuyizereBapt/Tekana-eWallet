# Generated by Django 4.1.4 on 2023-01-03 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0003_transaction_available_account_balance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='available_account_balance',
            new_name='account_balance_before',
        ),
    ]
