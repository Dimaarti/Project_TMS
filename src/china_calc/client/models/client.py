from django.db import models

from china_calc.account.models import User
from config.models import BaseModel


class Client(BaseModel):
    user = models.ForeignKey(
        User,
        related_name='clients',
        on_delete=models.CASCADE
    )
    full_name = models.CharField(
        max_length=128,
    )
    phone = models.CharField(
        max_length=50,
    )
    email = models.EmailField(
        max_length=64,
    )
    country = models.CharField(
        max_length=64,
    )
    city = models.CharField(
        max_length=64,
    )

    def __str__(self):
        return f'{self.full_name}'

    class Meta:
        db_table = 'client'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'