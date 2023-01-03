from django.urls import path
from .views import AcountFundsTransferView, TransactionsListView

urlpatterns = [
    path('transfer', AcountFundsTransferView.as_view(), name="account-funds-transfer"),
    path('<str:account_uuid>/transactions', TransactionsListView.as_view(), name="list-account-transactions"),
]