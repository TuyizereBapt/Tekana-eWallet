import typing
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework.test import APIClient


def generate_drf_http_response(
    data: typing.Dict,
    status_code: int,
    message: str = None,
    errors=None
):
    """Wrapper function for generating http responses

    Returns: rest_framework.response.Response
        TemplateResponse that returns appropriate data to return to the client

    Parameters
    ----------
    message: bool
        Human friendly message that can be communicated to users by the client
    data: bool
        Data the client is actually requesting for
    status_code: bool
        The status code of the response
    errors: list or dict
        Any errors incurred in the operation.
        Bear in mind, some operations can be successful with errors (fault tolerance)

    Examples
    ----------
    >>> class ProviderChargeItemListView(APIView):
    >>>     permission_classes = [permissions.IsAuthenticated]

    >>>     def get(self, request, provider_id=None, patient_id=None):
    >>>         charge_items = ChargeItem.objects.filter(provider=provider_id, patient=patient_id)
    >>>
    >>>         serializer = ChargeItemSerializer(charge_items, many=True)
    >>>         data = serializer.data
    >>>         message = "Successfully retrieved charge items"
    >>>         success = True
    >>>         status_code = status.HTTP_200_OK

    >>>         return generate_drf_http_response(success=success,
    >>>                                       message=message,
    >>>                                       data=data,
    >>>                                       errors=errors,
    >>>                                       status_code=status_code)
    """
    if message is None:
        if isinstance(errors, AssertionError):
            message = str(errors)

        elif isinstance(errors, KeyError):
            message = f"{str(errors)} was not found during this operation"

        elif isinstance(errors, (ValidationError, APIException)):
            message = errors.detail.popitem()[0] if isinstance(
                errors.detail, dict) else str(errors.detail[0])

        elif isinstance(errors, Exception):
            message = f"An error occurred and we could not complete this operation: {errors}"
        errors = str(errors)

    payload = {
        "message": message,
        "data": data,
        "errors": errors
    }
    return Response(data=payload, status=status_code)

class BaseAPITestCase(APITestCase):
    def setUp(self):
        from registration.models import AuthUser as User
        from django.urls import reverse

        # Set the client to use in making API calls
        self.client = APIClient()

        # Create a user to use in authentication & authorization
        email = "test@example.com"
        password = "testpassword"
        self.test_user = User.objects.create_user(email=email, password=password)

        # Authenticate the test_user
        url = reverse('token_obtain_pair')
        data = {"email": email, "password": password}
        response = self.client.post(url, data, format='json')

        # Set authorization token for subsequest API calls that require authorization
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data["access"])
