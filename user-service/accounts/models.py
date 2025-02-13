from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from enum import Enum

class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', 'Administrator'
    MANAGER = 'MANAGER', 'Manager'
    STAFF = 'STAFF', 'Staff'
    PREMUIM_USER = 'PREMUIM_USER', 'Premuim User'
    COMMON_USER = 'COMMON_USER', 'Common User'

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20, default='', null=False)
    last_name = models.CharField(blank=True, default='', null=False)
    provider = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.URLField(blank=True, null=True)
    joined_at = models.DateField(auto_now_add=True)
    last_login = models.DateField(auto_now=True)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.COMMON_USER
    )
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email   
    
    def social_login(self, provider, social_account):
        self.provider = provider
        if not self.profile_picture:
            self.profile_picture = social_account.extra_data.get('picture')
        self.save()

    def has_admin_permission(self):
        return self.role == UserRole.ADMIN

    def has_manager_permission(self):
        return self.role in [UserRole.ADMIN, UserRole.MANAGER]