# serializers.py
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, UserRole
from django.core.exceptions import ValidationError


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'first_name', 'last_name','phone', 'birth_date', 'profile_picture']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }

    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 
                 'birth_date', 'profile_picture', 'role', 'is_active']
        read_only_fields = ['joined_at', 'last_login']

    def validate_role(self, value):
        if value not in UserRole.values:
            raise ValidationError(f"Invalid role. Must be one of {UserRole.values}")
        return value
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'username': self.user.username
        }
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
