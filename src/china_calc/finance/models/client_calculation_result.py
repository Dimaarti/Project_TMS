from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ClientCalculationResult(models.Model):
    calculation_result = models.ForeignKey(
        to="CalculationResult",
        on_delete=models.CASCADE,
        related_name="client_results",
        verbose_name="Общий результат расчета",
    )

    client = models.ForeignKey(
        to="client.Client",
        on_delete=models.PROTECT,
        related_name="client_calculation_results",
        verbose_name="Клиент",
    )

    commission_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal(0)), MaxValueValidator(Decimal(100))],
        verbose_name="Комиссия байера, %",
    )

    purchase_cost = models.DecimalField(
        max_digits=14, decimal_places=2, default=0, verbose_name="Себестоимость товаров"
    )

    client_purchase_cost = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
        verbose_name="Стоимость товаров для клиента",
    )

    logistics_cost = models.DecimalField(
        max_digits=14, decimal_places=2, default=0, verbose_name="Доля логистики"
    )

    expenses_cost = models.DecimalField(
        max_digits=14, decimal_places=2, default=0, verbose_name="Расходы клиента"
    )

    buyer_commission_cost = models.DecimalField(
        max_digits=14, decimal_places=2, default=0, verbose_name="Комиссия байера"
    )

    price_cost = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
        verbose_name="Себестоимость по клиенту",
    )

    client_price_cost = models.DecimalField(
        max_digits=14, decimal_places=2, default=0, verbose_name="Итого клиенту"
    )

    profit_cost = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    class Meta:
        ordering = ["client__full_name"]
        verbose_name = "Результат расчета клиента"
        verbose_name_plural = "Результаты расчетов клиентов"

    def __str__(self):
        return f"{self.client} - {self.calculation_result.shipment.number}"
