from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from config.base_models import BaseModel
from config.model_choices import Currency


class ClientPayment(BaseModel):
    shipment = models.ForeignKey(
        to="shipment.Shipment",
        on_delete=models.CASCADE,
        related_name="client_payments",
        verbose_name="Поставка",
    )

    client = models.ForeignKey(
        to="client.Client",
        on_delete=models.PROTECT,
        related_name="payments",
        verbose_name="Клиент",
    )

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name="Сумма оплаты",
    )

    currency = models.CharField(
        max_length=3, choices=Currency.choices, verbose_name="Валюта"
    )

    paid_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")

    note = models.CharField(max_length=255, blank=True, verbose_name="Примечание")

    class Meta:
        ordering = ["-paid_at"]
        verbose_name = "Оплата клиента"
        verbose_name_plural = "Оплаты клиентов"

    def __str__(self):
        return f"{self.client}: {self.amount}{self.currency}по поставке {self.shipment}"

    def clean(self):
        super().clean()

        if not self.shipment_id or not self.client_id:
            return

        if self.shipment.user_id != self.client.user_id:
            raise ValidationError(
                {"client": "Клиент и поставка должны принадлежать одному пользователю"}
            )

        if not self.shipment.items.filter(client_id=self.client.id).exists():
            raise ValidationError(
                {"client": "У клиента нет товаров в выбранной поставке"}
            )
