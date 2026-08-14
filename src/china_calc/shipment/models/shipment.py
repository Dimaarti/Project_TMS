
from django.db import models

from config.base_models import BaseModel
from config.model_choices import (
    Currency,
    LogisticCalculationMethod,
    SettlementFinalCurrency,
    ShipmentStatus,
)


class Shipment(BaseModel):
    user = models.ForeignKey(
        to="account.User",
        on_delete=models.CASCADE,
        related_name="shipments",
        verbose_name="Пользователь",
    )

    route = models.ForeignKey(
        to="logistics.Route",
        on_delete=models.PROTECT,
        related_name="shipments",
        verbose_name="Маршрут поставки",
    )

    exchange_rate = models.ForeignKey(
        to="finance.ExchangeRate",
        on_delete=models.PROTECT,
        related_name="shipments",
        verbose_name="Обменные курсы валют",
    )

    number = models.CharField(max_length=30, verbose_name="Номер поставки")

    status = models.CharField(
        max_length=20,
        choices=ShipmentStatus,
        default=ShipmentStatus.EDITE,
        verbose_name="Статус поставки",
    )

    logistic_calculation_type = models.CharField(
        max_length=30,
        choices=LogisticCalculationMethod.choices,
        default=LogisticCalculationMethod.WEIGHT,
        verbose_name="Способ расчета логистики",
    )

    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Фактический вес поставки, кг",
    )

    volume = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Фактический объем поставки, м3",
    )

    tariff_one_kg = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Тариф за 1 кг"
    )

    tariff_one_m3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Тариф за 1 м3"
    )

    tariff_currency = models.CharField(
        max_length=10,
        choices=Currency.choices,
        default="USD",
        verbose_name="Валюта тарифа",
    )

    settlement_final_currency = models.CharField(
        max_length=10,
        choices=SettlementFinalCurrency.choices,
        default=SettlementFinalCurrency.BYN,
        verbose_name="Валюта итогового расчета",
    )

    note = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Примечание"
    )

    class Meta:
        ordering = ["-created_at"]
        db_table = "shipment"
        verbose_name = "Поставка"
        verbose_name_plural = "Поставки"

        constraints = [
            models.UniqueConstraint(
                fields=["user", "number"], name="unique_shipment_number_per_user"
            )
        ]

    def __str__(self):
        return self.number

    def invalidate_calculations(self):
        """Помечает предыдущий расчёт неактуальным после изменения поставки."""
        self.calculation_results.filter(is_actual=True).update(is_actual=False)
