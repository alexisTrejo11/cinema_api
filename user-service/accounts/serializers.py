from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema_serializer, extend_schema_field
from .models import User, UserRole
from django.core.exceptions import ValidationError

@extend_schema_serializer(
    examples=[
        {
            "email": "user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "SecurePassword123!",
            "username": "johndoe",
            "phone": "123456789",
            "birth_date": "1990-01-01",
            "profile_picture": "https://example.com/profile.jpg"
        }
    ]
)
class UserSignupSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Handles the creation of new user accounts by validating input data
    and hashing the password before saving the user.
    """

    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'username', 'phone', 'birth_date', 'profile_picture']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'first_name': {"required": True},
            'last_name': {"required": True}
        }


@extend_schema_serializer(
    examples=[
        {
            "id": 1,
            "email": "user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "123456789",
            "birth_date": "1990-01-01",
            "profile_picture": "https://example.com/profile.jpg",
            "role": "common_user",
            "is_active": True
        }
    ]
)
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving user details.

    Provides basic user information such as email, name, phone number,
    birth date, and profile picture. It also includes the user's role
    and active status.
    """

    @extend_schema_field(str)
    def validate_role(self, value):
        """
        Validates the user role.

        Ensures the role is one of the predefined values in UserRole.
        """
        if value not in UserRole.values:
            raise ValidationError(f"Invalid role. Must be one of {UserRole.values}")
        return value

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 
                  'birth_date', 'profile_picture', 'role', 'is_active']
        read_only_fields = ['joined_at', 'last_login']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer for obtaining authentication tokens.

    Extends the default JWT serializer to include user details
    in the response.
    """

    def validate(self, attrs):
        """
        Validates user credentials and returns tokens with additional user details.
        """
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'username': self.user.username
        }
        return data

    @classmethod
    def get_token(cls, user):
        """
        Generates a JWT token with additional user information.
        """
        token = super().get_token(user)
        token['email'] = user.email
        return token


@extend_schema_serializer(
    examples=[
        {
            "email": "user@example.com",
            "password": "SecurePassword123!"
        }
    ]
)
class LoginSerializer(serializers.Serializer):
    """
    Serializer for user authentication.

    Requires an email and password to authenticate the user.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
