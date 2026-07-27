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
        verbose_name='Полное имя'
    )
    phone = models.CharField(
        max_length=50,
        verbose_name='Телефон'
    )
    address = models.CharField(
        max_length=300,
        verbose_name='Адрес',
        blank=True,
        null=True
    )

    buyer_commission_percent = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Комиссия байера, %'
    )

    class Meta:
        db_table = 'client'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.full_name}'
