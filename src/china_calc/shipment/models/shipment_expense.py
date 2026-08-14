from django.core.exceptions import ValidationError
from django.db import models

from config.base_models import BaseModel
from config.model_choices import Currency, ExpenseType


class ShipmentExpense(BaseModel):
    shipment = models.ForeignKey(
        to="Shipment",
        on_delete=models.CASCADE,
        related_name="expenses",
        verbose_name="Поставка",
    )

    item = models.ForeignKey(
        to="ShipmentItem",
        on_delete=models.CASCADE,
        related_name="expenses",
        null=True,
        blank=True,
        verbose_name="Конкретный товар",
    )

    expense_type = models.CharField(
        max_length=40, choices=ExpenseType.choices, verbose_name="Тип расходов"
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")

    currency = models.CharField(
        max_length=10,
        choices=Currency.choices,
        default=Currency.USD,
        verbose_name="Валюта",
    )

    note = models.CharField(
        max_length=250, null=True, blank=True, verbose_name="Примечание"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Расход поставки"
        verbose_name_plural = "Расходы поставки"

    def __str__(self):
        return self.get_expense_type_display()

    def clean(self):
        super().clean()
        if self.item_id is not None and self.item.shipment_id != self.shipment_id:
            raise ValidationError(
                {"item": "Товар расхода должен принадлежать выбранной поставке."}
            )
