from .models import User
from .utils import Result
from rest_framework_simplejwt.tokens import RefreshToken
import re
from django.db import transaction
from django.contrib.auth import authenticate
from wallet.services import WalletService

class UserService:
    def create(self, data):
        user = User.objects.create_user(
            email=data['email'],
            username=data['username'],
            password=data['password'],
            phone=data.get('phone', ''),
            birth_date=data.get('birth_date'),
            profile_picture=data.get('profile_picture')
        )
        return user


class AuthService:
    def __init__(self):
        self.wallet_service = WalletService()

    def validate_signup_credentials(self, data):
        email_result = self.__validate_email(data.get('email')) 
        if not email_result.is_success:
            return email_result
        
        username = data.get('username')
        if username:
            username_result = self.__validate_username(username) 
            if not username_result.is_success():
                return username_result
            
        password_result = self.__validate_password(data.get('password'))
        if not password_result.is_success():
            return password_result

        return Result.success()
    
    def validate_login(self, data):
        user = authenticate(
            username=data.get('email'),  
            password=data.get('password')  
        )

        if not user:
            return Result.error('Invalid email or password.')
        
        return Result.success(user)

    
    def procces_signup(self, user : User):
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        self.wallet_service.init_wallet(user)

        return {'access': str(access),'refresh': str(refresh)}

    def procces_login(self, user : User):
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return {'access': str(access),'refresh': str(refresh)}
    
    def proccess_logout(self, refresh_token):
        token = RefreshToken(refresh_token)
        token.blacklist()

    def __validate_password(password) -> Result:
        if len(password) < 8:
            return Result.error("Password must be at least 8 characters long.")

        if not re.search(r'[A-Z]', password):
            return Result.error("Password must contain at least one uppercase letter.")

        if not re.search(r'[a-z]', password):
            return Result.error("Password must contain at least one lowercase letter.")

        if not re.search(r'[@$!%*?&]', password):
            return Result.error("Password must contain at least one special character like @, $, !, %, *, ?, &.")

        return Result.success("Password is valid.")
    

    def __validate_email(self, email) -> Result:
        email_account = User.objects.filter(email=email).exists()
        if email_account:
            return Result.error("email already taken")
        
        return Result.success()
    
    def __validate_username(self, username) -> Result:
        username_account = User.objects.filter(username=username).exists()
        if username_account:
            return Result.error("username already taken")
        
        return Result.success()