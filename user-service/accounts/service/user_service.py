import logging
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import transaction
from ..models import User

logger = logging.getLogger(__name__)

class UserService:
    CACHE_TIMEOUT = 60 * 15

    def __init__(self):
        self.model = User

    @transaction.atomic
    def create_user(self, data):
        user = self.model(**data)
        user.set_password(data.get('password'))
        user.full_clean()
        user.save()
        
        cache.set(f"user_{user.id}", user, self.CACHE_TIMEOUT)
        logger.info(f"User created: {user.id} - {user.email}")

        return user

    def update_user(self, user_id, data):
        user = self.get_user_by_id(user_id)

        for key, value in data.items():
            setattr(user, key, value)

        user.full_clean()
        user.save()

        cache.set(f"user_{user.id}", user, self.CACHE_TIMEOUT)
        logger.info(f"User updated: {user.id}")

        return user

    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        user.is_active = False
        user.save()

        cache.delete(f"user_{user.id}")
        logger.warning(f"User deactivated: {user.id}")

        return user

    def get_user_by_id(self, user_id):
        cache_key = f"user_{user_id}"
        user = cache.get(cache_key)

        if not user:
            try:
                user = self.model.objects.get(id=user_id)
                cache.set(cache_key, user, self.CACHE_TIMEOUT)  
            except self.model.DoesNotExist:
                logger.error(f"User not found: {user_id}")
                raise ValidationError(f"User with id {user_id} does not exist")

        return user

    def get_active_users(self):
        cache_key = "active_users"
        users = cache.get(cache_key)

        if not users:
            users = list(self.model.objects.filter(is_active=True))
            cache.set(cache_key, users, self.CACHE_TIMEOUT)

        return users

    def get_users_by_role(self, role):
        cache_key = f"users_role_{role}"
        users = cache.get(cache_key)

        if not users:
            users = list(self.model.objects.filter(role=role, is_active=True))
            cache.set(cache_key, users, self.CACHE_TIMEOUT)

        return users
