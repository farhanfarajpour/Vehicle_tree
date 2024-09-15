from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django_prometheus.models import ExportModelOperationsMixin
from vehicle_tree_app.models.base import BaseModel


class CustomUserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """Create and save a User with the given mobile and password."""

        if not username:
            raise ValueError('The given mobile must be set')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        """Create and save a regular User with the given mobile and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        """Create and save a SuperUser with the given mobile and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username=username, password=password, **extra_fields)


class Users(ExportModelOperationsMixin("users"), AbstractUser, BaseModel):

    username = models.CharField(
        max_length=150, unique=True, null=True, blank=True, verbose_name="username", name="username")
    mobile = models.CharField(
        max_length=20, null=True, blank=True, unique=True, verbose_name="mobile", name="mobile")

    is_active = models.BooleanField(
        default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.username

    def save(self, *args, **kwargs):
        # self.u_invitationCode = self.mobile
        super().save(*args, **kwargs)
