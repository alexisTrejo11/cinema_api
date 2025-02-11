from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20, default='', null=False)
    last_name = models.CharField(blank=True, default='', null=False)
    provider = models.CharField(null=True)
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.URLField(blank=True, null=True)
    joined_at = models.DateField(auto_now_add=True)
    last_login = models.DateField(auto_now=True)

    def __str__(self):
        return self.email   