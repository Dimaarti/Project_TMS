from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from config.base_models import BaseModel


class Client(BaseModel):
    user = models.ForeignKey(
        to="account.User",
        related_name="clients",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    full_name = models.CharField(max_length=128, verbose_name="Полное имя")

    phone = models.CharField(max_length=50, verbose_name="Телефон")
    address = models.CharField(
        max_length=300, verbose_name="Адрес", blank=True, null=True
    )

    buyer_commission_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(Decimal(0)),
            MaxValueValidator(Decimal(100)),
        ],
        verbose_name="Комиссия байера, %",
    )

    class Meta:
        ordering = ["full_name"]
        db_table = "clients"
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.full_name
