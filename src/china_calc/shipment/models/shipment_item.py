from django.db import models

from config.model_choices import Currency
from config.models import BaseModel


class ShipmentItem(BaseModel):
    shipment = models.ForeignKey(
        to='Shipment',
        on_delete=models.CASCADE,
        related_name='item',
        verbose_name='Поставка'
    )

    client = models.ForeignKey(
        to='client.Client',
        on_delete=models.CASCADE,
        related_name='item',
        verbose_name='Клиент'
    )

    product = models.ForeignKey(
        to='Product',
        on_delete=models.CASCADE,
        related_name='item',
        verbose_name='Товар'
    )

    tracking_number = models.CharField(
        max_length=130,
        null=True,
        blank=True,
        verbose_name='Трек-номер'
    )

    product_link = models.URLField(
        null=True,
        blank=True,
        verbose_name='Ссылка на товар'
    )

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество, шт'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена за единицу'
    )

    price_currency = models.CharField(
        max_length=10,
        choices=Currency.choices,
        default=Currency.CNY,
        verbose_name='Валюта цены'
    )

    inspection_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Проверка товара'
    )

    photo_report_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Фотоотчет'
    )

    packaging_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Упаковка'
    )

    class Meta:
        ordering = ['-quantity', '-price']
        verbose_name = "Товар для отправки"
        verbose_name_plural = "Товары для отправки"

    def __str__(self):
        return self.product.name
