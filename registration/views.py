from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer
from rest_framework import permissions
from .serializers import RegisterSerializer, UserSerializer
from .models import AuthUser as User
from wallets.models import Account
from base.utils import generate_drf_http_response
from rest_framework.exceptions import ValidationError


class UserRegistrationView(APIView):
    serializer_class = RegisterSerializer

    # Allow anyone to register users
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """
        Register users

        """
        serializer = RegisterSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            # Create an account for the registered user. Every user should have an account
            Account.objects.create(owner=user, name="Primary")
            
            return generate_drf_http_response(
                data=UserSerializer(user).data,
                message="User Created Successfully. Login to get authorization token",
                status_code=status.HTTP_201_CREATED
            )
        except (ValidationError, Exception) as e:

            if isinstance(e, ValidationError):
                errors = serializer.error_messages
            else:
                errors = str(e)

            return generate_drf_http_response(
                data=None,
                message="Registering user failed",
                status_code=status.HTTP_400_BAD_REQUEST,
                errors=errors
            )


class RegisteredUsersView(APIView):
    serializer_class = UserSerializer

    def get(self, request):
        """
        Get all non-deleted registered users
        """
        users = User.objects.filter(is_deleted=False)
        serializer = UserSerializer(users, many=True)
        return generate_drf_http_response(
            data=serializer.data,
            message="Users successfully fetched!",
            status_code=status.HTTP_200_OK
        )
