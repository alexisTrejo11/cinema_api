from ..models import User
from ..utils import Result
from rest_framework_simplejwt.tokens import RefreshToken
import re
from django.db import transaction
from django.contrib.auth import authenticate
from wallet.services import WalletService

from django.core.exceptions import ValidationError
from django.db import transaction

class UserService:
    def __init__(self):
        self.model = User

    @transaction.atomic
    def create_user(self, data):
        user = self.model(**data)
        user.set_password(data.get('password'))
        user.full_clean()
        user.save()
        return user

    def update_user(self, user_id, data):
        user = self.get_user_by_id(user_id)
        for key, value in data.items():
            setattr(user, key, value)
        user.full_clean()
        user.save()
        return user

    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        user.is_active = False
        user.save()
        return user

    def get_user_by_id(self, user_id):
        try:
            return self.model.objects.get(id=user_id)
        except self.model.DoesNotExist:
            raise ValidationError(f"User with id {user_id} does not exist")

    def get_active_users(self):
        return self.model.objects.filter(is_active=True)

    def get_users_by_role(self, role):
        return self.model.objects.filter(role=role, is_active=True)
