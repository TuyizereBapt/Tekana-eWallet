from django.urls import reverse
from registration.models import AuthUser as User
from rest_framework import status
from base.utils import BaseAPITestCase
from wallets.models import Account


class TransferTests(BaseAPITestCase):
    def setUp(self):
        self.authorize_requests()

        self.primary_account = Account.objects.create(
            owner=self.test_user, name="Primary", balance=100
        )
        self.secondary_account = Account.objects.create(
            owner=self.test_user, name="Secondary"
        )
        self.url = "/api/accounts/transfer"

    def test_transfer_account_funds(self):
        

        data = {
            "sender_account_uuid": self.primary_account.uuid,
            "receiver_account_uuid": self.secondary_account.uuid,
            "amount": 25,
            "reason": "Payment"
        }
        
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the transfer returns two transactions
        self.assertEqual(len(response.data["data"]), 2)

    def test_transfer_more_than_account_balance(self):
        data = {
            "sender_account_uuid": self.primary_account.uuid,
            "receiver_account_uuid": self.secondary_account.uuid,
            "amount": 1000,
            "reason": "Payment"
        }
        
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_transfer_negative_amount(self):
        data = {
            "sender_account_uuid": self.primary_account.uuid,
            "receiver_account_uuid": self.secondary_account.uuid,
            "amount": -50,
            "reason": "Payment"
        }
        
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
