from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from china_calc.account.managers import UserManager
from config.models import BaseModel


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    first_name = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=64,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        max_length=64,
        unique=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    class Meta:
        db_table = "user"
        verbose_name_plural = "Users"
        verbose_name = "User"
