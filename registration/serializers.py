from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import AuthUser as User
from wallets.serializers import AccountSerializer


class UserSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(
    #     required=True,
    #     validators=[UniqueValidator(queryset=User.objects.all())]
    # )
    # password = serializers.CharField(min_length=8)

    accounts = AccountSerializer(many=True, required=False)

    class Meta:
        model = User
        exclude = ('id', 'password', 'is_superuser')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data) -> User:
        user = User.objects.create_user(
            validated_data['email'], password=validated_data['password'], 
            first_name=validated_data['first_name'], last_name=validated_data['last_name']
        )
        return user
