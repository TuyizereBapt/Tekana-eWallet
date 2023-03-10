from django.db import models
from base.models import TimeStampedModel
from base.constants.models import AppModels
from .choices import TransactionStatusTypes
from django.db.models import CheckConstraint, Q


class Account(TimeStampedModel):
    """
    This model represents User Accounts (eWallets) that are used to transfer or receive money
    """
    balance = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    account_type = models.CharField(max_length=15, null=True)
    owner = models.ForeignKey(
        AppModels.USER, on_delete=models.DO_NOTHING, related_name='accounts')
    name = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = "wallet_accounts"
        constraints = [
            # Ensures the balance field is never less than 0
            CheckConstraint(check=Q(balance__gte=0), name='balance_gte_0')
        ]


class Transaction(TimeStampedModel):
    """
    Transactions done between accounts
    """
    sender_account = models.ForeignKey(
        AppModels.ACCOUNT, on_delete=models.DO_NOTHING, related_name='debit_transactions')
    receiver_account = models.ForeignKey(
        AppModels.ACCOUNT, on_delete=models.DO_NOTHING, related_name='credit_transactions')
    amount = models.FloatField()
    status = models.CharField(default=TransactionStatusTypes.PENDING,
                              choices=TransactionStatusTypes.choices, max_length=15)
    reason = models.CharField(max_length=50, default='')
    notes = models.TextField(default='')
    transaction_type = models.CharField(max_length=15, null=True)
    account_balance_before = models.FloatField(verbose_name="Account's balance before the transaction", null=True)
    account_balance_after = models.FloatField(verbose_name="Account's balance after the transaction", null=True)

    class Meta:
        db_table = "wallet_transactions"
        indexes = [
            models.Index(fields=['-created_at',], name='created_at_desc_idx'),
        ]
