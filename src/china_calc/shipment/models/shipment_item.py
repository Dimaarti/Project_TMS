from django.core.exceptions import ValidationError
from django.db import models

from config.base_models import BaseModel
from config.model_choices import Currency


class ShipmentItem(BaseModel):
    shipment = models.ForeignKey(
        to="Shipment",
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Поставка",
    )

    client = models.ForeignKey(
        to="client.Client",
        on_delete=models.PROTECT,
        related_name="shipment_items",
        verbose_name="Клиент",
    )

    name = models.CharField(max_length=100, verbose_name="Наименование товара")

    tracking_number = models.CharField(
        max_length=130, null=True, blank=True, verbose_name="Трек-номер"
    )

    product_link = models.URLField(
        null=True, blank=True, verbose_name="Ссылка на товар"
    )

    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество, шт")

    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за единицу"
    )

    price_currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.CNY,
        verbose_name="Валюта цены",
    )

    weight = models.DecimalField(
        max_digits=10, decimal_places=3, default=0, verbose_name="Общий вес позиции, кг"
    )

    volume = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        default=0,
        verbose_name="Общий объем позиции, м3",
    )

    class Meta:
        ordering = ["-client_id", "-name"]
        verbose_name = "Товар для отправки"
        verbose_name_plural = "Товары для отправки"

    def __str__(self):
        return f"{self.name} - {self.client.full_name}"

    def clean(self):
        super().clean()

        if not self.shipment_id or not self.client_id:
            return

        if self.shipment.user_id != self.client.user_id:
            raise ValidationError(
                {"client": "Клиент и поставка должны принадлежать одному пользователю"}
            )
