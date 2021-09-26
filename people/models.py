from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


class Customer(models.Model):
    name = models.CharField(max_length=255, null=False)
    document = models.CharField(max_length=11, null=False)


class UserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password=None, **kwargs):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.is_admin = False
        user.is_staff = False
        user.save(using=self._db)
        return user


class User(AbstractUser):
    objects = UserManager()
