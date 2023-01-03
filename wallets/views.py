from rest_framework.views import APIView
from rest_framework import status, permissions
from django.db.models import F
from django.db import transaction as django_transaction
from rest_framework.exceptions import ValidationError
from base.utils import generate_drf_http_response
from .models import Account, Transaction
from .serializers import TransactionSerializer
from .choices import TransactionStatusTypes, TransactionTypes


class AcountFundsTransferView(APIView):
    def post(self, request):
        """
        Tranfer money from one account to another
        Params:
            request
        """
        from .exceptions import InvalidTransactionException

        try:
            amount = request.data['amount']
            reason = request.data.get('reason', '')
            notes = request.data.get('notes', '')
            sender_account_uuid = request.data['sender_account_uuid']
            receiver_account_uuid = request.data['receiver_account_uuid']

            if amount <= 0:
                raise InvalidTransactionException(
                    'The amount to transfer cannot be 0 or less than 0.')

            # Select accounts and lock matched database rows to prevent race conditions
            sender_account = Account.objects.select_for_update().get(uuid=sender_account_uuid)
            receiver_account = Account.objects.select_for_update().get(uuid=receiver_account_uuid)

            # Check if the sender_account has enough amount to transfer
            if sender_account.balance - amount < 0:
                raise InvalidTransactionException(
                    "Insuficient balance. The amount to transfer is more than the availbale account's balance")

            with django_transaction.atomic():
                # Get the balance before the operation to store in the transaction details
                sender_account_balance = sender_account.balance
                sender_account.balance = sender_account_balance - amount

                receiver_account_balance = receiver_account.balance
                receiver_account.balance = receiver_account_balance + amount
                sender_account.save()
                receiver_account.save()

                # Record the transaction details. Create two transactions for both the debit and credit operations
                debit_transaction = Transaction(
                    sender_account=sender_account,
                    receiver_account=receiver_account,
                    amount=amount,
                    reason=reason,
                    notes=notes,
                    status=TransactionStatusTypes.COMPLETE,
                    transaction_type=TransactionTypes.DEBIT,
                    account_balance_before=sender_account_balance,
                    account_balance_after = sender_account.balance
                )
                credit_transaction = Transaction(
                    sender_account=sender_account,
                    receiver_account=receiver_account,
                    amount=amount,
                    reason=reason,
                    notes=notes,
                    status=TransactionStatusTypes.COMPLETE,
                    transaction_type=TransactionTypes.CREDIT,
                    account_balance_before=receiver_account_balance,
                    account_balance_after=receiver_account.balance
                )

                transactions = Transaction.objects.bulk_create(
                    [debit_transaction, credit_transaction])

                response = generate_drf_http_response(
                    data=TransactionSerializer(transactions, many=True).data,
                    message="The transfer transaction was successful!",
                    status_code=status.HTTP_200_OK
                )

        except Exception as e:
            error = "Transfer failed!"

            if isinstance(e, KeyError):
                error = f"{error} {e} is required."
            elif isinstance(e, InvalidTransactionException):
                error = f"{error} {e.message}"
            else:
                error = f"{error} {e.args[0]}"

            response = generate_drf_http_response(
                data=None,
                message="The transfer transaction failed",
                status_code=status.HTTP_400_BAD_REQUEST,
                errors=error
            )

        return response


class TransactionsListView(APIView):
    def get(self, request, account_uuid):
        """
        List all transactions done with an account
        """
        from rest_framework.pagination import PageNumberPagination
        from django.db.models import Q

        transactions = Transaction.objects.filter(
            Q(sender_account__uuid=account_uuid,
              transaction_type=TransactionTypes.DEBIT)
            | Q(receiver_account__uuid=account_uuid,
                transaction_type=TransactionTypes.CREDIT)).order_by('-created_at')

        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items to be returned per page
        result_page = paginator.paginate_queryset(transactions, request)

        serializer = TransactionSerializer(result_page, many=True)

        return generate_drf_http_response(
            data=serializer.data,
            message="Transactions were successfully retrieved!",
            status_code=status.HTTP_200_OK
        )
