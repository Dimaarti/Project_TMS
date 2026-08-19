from django.db import models

from config.base_models import BaseModel
from config.model_choices import Currency


class CalculationResult(BaseModel):
    shipment = models.ForeignKey(
        to="shipment.Shipment",
        on_delete=models.CASCADE,
        related_name="calculation_results",
        verbose_name="Поставка",
    )

    exchange_rate = models.ForeignKey(
        to="ExchangeRate",
        on_delete=models.PROTECT,
        related_name="calculation_results",
        verbose_name="Обменный курс",
    )

    purchase_currency = models.CharField(
        max_length=3,
        choices=Currency,
        default=Currency.CNY,
        verbose_name="Основная валюта товаров",
    )

    final_currency = models.CharField(
        max_length=3,
        choices=Currency,
        default=Currency.BYN,
        verbose_name="Итоговая валюта",
    )

    purchase_cost = models.DecimalField(
        max_digits=16, decimal_places=2, default=0, verbose_name="Стоимость товара"
    )

    client_purchase_cost = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
        verbose_name="Стоимость товара для клиента",
    )

    logistics_cost = models.DecimalField(
        max_digits=16, decimal_places=2, default=0, verbose_name="Логистические расходы"
    )

    logistics_cost_rub = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
        editable=False,
        verbose_name="Общая стоимость доставки в RUB",
    )

    buyer_commission_cost = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
        verbose_name="Расчет комиссии байера, %",
    )

    price_cost = models.DecimalField(
        max_digits=16, decimal_places=2, default=0, verbose_name="Общая себестоимость"
    )

    client_price_cost = models.DecimalField(
        max_digits=16, decimal_places=2, default=0, verbose_name="Итого для клиентов"
    )

    profit_cost = models.DecimalField(
        max_digits=16, decimal_places=2, default=0, verbose_name="Прибыль"
    )

    expenses_cost = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
        verbose_name="Расходы",
    )

    is_actual = models.BooleanField(default=True, verbose_name="Актуальный расчет")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Результат расчета"
        verbose_name_plural = "Результаты расчетов"

        constraints = [
            models.UniqueConstraint(
                fields=["shipment"],
                condition=models.Q(is_actual=True),
                name="unique_actual_calculation_per_shipment",
            )
        ]

    def __str__(self):
        return f"Расчет поставки {self.shipment.number}"
