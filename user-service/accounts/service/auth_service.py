import logging
import re
from django.core.cache import cache
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import User
from ..utils import Result
from wallet.services import WalletService

logger = logging.getLogger(__name__)

class AuthService:
    CACHE_TIMEOUT = 60 * 15

    def __init__(self):
        self.wallet_service = WalletService()

    def validate_signup_credentials(self, data):
        email_result = self.__validate_email(data.get('email')) 
        if not email_result.is_success:
            logger.warning(f"Signup failed: {email_result.message}")
            return email_result
        
        username = data.get('username')
        if username:
            username_result = self.__validate_username(username) 
            if not username_result.is_success():
                logger.warning(f"Signup failed: {username_result.message}")
                return username_result
            
        password_result = self.__validate_password(data.get('password'))
        if not password_result.is_success():
            logger.warning(f"Signup failed: {password_result.message}")
            return password_result

        return Result.success()
    
    def validate_login(self, data):
        logger.info(f"Login attempt for: {data.get('email')}")
        user = authenticate(
            username=data.get('email'),  
            password=data.get('password')  
        )

        if not user:
            logger.warning(f"Login failed for: {data.get('email')}")
            return Result.error('Invalid email or password.')
        
        return Result.success(user)

    
    def procces_signup(self, user: User):
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        self.wallet_service.init_wallet(user)

        cache.set(f"user_{user.id}", user, self.CACHE_TIMEOUT)
        logger.info(f"User signed up: {user.email}")

        return {'access': str(access), 'refresh': str(refresh)}

    def procces_login(self, user: User):
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        cache.set(f"user_{user.id}", user, self.CACHE_TIMEOUT)
        logger.info(f"User logged in: {user.email}")

        return {'access': str(access), 'refresh': str(refresh)}
    
    def proccess_logout(self, refresh_token):
        token = RefreshToken(refresh_token)
        token.blacklist()
        logger.info("User logged out.")

    def __validate_password(self, password) -> Result:
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
        cache_key = f"user_email_{email}"
        email_account = cache.get(cache_key)

        if email_account is None:
            email_account = User.objects.filter(email=email).exists()
            cache.set(cache_key, email_account, self.CACHE_TIMEOUT)

        if email_account:
            return Result.error("Email already taken")
        
        return Result.success()
    
    def __validate_username(self, username) -> Result:
        cache_key = f"user_username_{username}"
        username_account = cache.get(cache_key)

        if username_account is None:
            username_account = User.objects.filter(username=username).exists()
            cache.set(cache_key, username_account, self.CACHE_TIMEOUT)

        if username_account:
            return Result.error("Username already taken")
        
        return Result.success()
