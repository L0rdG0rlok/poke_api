from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class UserProfileManager(BaseUserManager):
    """User Profile Manager"""

    def create_user(self, email, password, username, **kwargs):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, username, **kwargs):
        """Create a superuser"""
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_superuser", True)
        user = self.create_user(email, password, username=username, **kwargs)
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """User Model"""

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserProfileManager()

    def __str__(self):
        return self.email


class Pokemon(models.Model):
    """Pokemon Model"""

    name = models.CharField(max_length=255)
    height = models.IntegerField()
    weight = models.IntegerField()
    sprite = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    owner = models.ForeignKey(
        "UserProfile", on_delete=models.CASCADE, related_name="Pokemon"
    )

    def __str__(self):
        return self.name
