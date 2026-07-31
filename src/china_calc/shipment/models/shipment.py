from django.db import models

from config.model_choices import (
    Currency,
    LogisticCalculationMethod,
    SettlementFinalCurrency,
)
from config.models import BaseModel


class Shipment(BaseModel):
    user = models.ForeignKey(
        to="account.User",
        on_delete=models.CASCADE,
        related_name="shipment",
    )

    route = models.ForeignKey(
        to="logistics.Route",
        on_delete=models.PROTECT,
        related_name="shipment",
        verbose_name="Маршрут поставки",
    )

    exchange_rate = models.ForeignKey(
        to="finance.ExchangeRate",
        on_delete=models.PROTECT,
        related_name="shipment",
        verbose_name="Обменные курсы валют",
    )

    tariff_one_kg = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Тариф за 1 кг"
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

    number = models.CharField(max_length=30, verbose_name="Номер поставки")

    status = models.CharField(
        max_length=30, default="Создана", verbose_name="Статус поставки"
    )

    weight = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Вес, кг"
    )

    volume = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Объем, м3"
    )

    logistic_calculation_type = models.CharField(
        max_length=30,
        choices=LogisticCalculationMethod.choices,
        default=LogisticCalculationMethod.WEIGHT,
        verbose_name="Способ расчета логистики",
    )

    tariff_one_m3 = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Тариф за 1 м3"
    )

    note = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Примечание"
    )

    class Meta:
        ordering = ["number"]
        db_table = "shipment"
        verbose_name = "Поставка"
        verbose_name_plural = "Поставки"

    def __str__(self):
        return self.number
