from rest_framework import serializers
from .models import Account, Transaction


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = (id,)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = (id,)
