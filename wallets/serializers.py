from rest_framework import serializers
from .models import Account, Transaction


class AccountSerializer(serializers.ModelSerializer):
    owner_user_uuid = serializers.ReadOnlyField(source="owner.uuid")
    class Meta:
        model = Account
        exclude = ('id', 'owner')


class TransactionSerializer(serializers.ModelSerializer):
    sender_account_uuid = serializers.ReadOnlyField(source="sender_account.uuid")
    receiver_account_uuid = serializers.ReadOnlyField(source="receiver_account.uuid")

    class Meta:
        model = Transaction
        exclude = ('id','sender_account', 'receiver_account')
