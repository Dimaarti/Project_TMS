from django.db import models

from config.model_choices import Currency, ExpenseType
from config.models import BaseModel


class ShipmentExpense(BaseModel):
    shipment = models.ForeignKey(
        to="Shipment",
        on_delete=models.CASCADE,
        related_name="expense",
    )

    item = models.ForeignKey(
        to="ShipmentItem",
        on_delete=models.CASCADE,
        related_name="expense",
        null=True,
        blank=True,
        verbose_name="Конкретный товар",
    )

    expense_type = models.CharField(
        max_length=40, choices=ExpenseType.choices, verbose_name="Тип расходов"
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")

    currency = models.CharField(
        max_length=10, choices=Currency.choices, verbose_name="Валюта", default=Currency.USD
    )

    note = models.CharField(
        max_length=250, null=True, blank=True, verbose_name="Примечание"
    )

    class Meta:
        ordering = ["-amount"]
        verbose_name_plural = "Расходы"

    def __str__(self):
        return self.expense_type
