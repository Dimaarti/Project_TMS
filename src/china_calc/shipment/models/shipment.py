from django.db import models

from china_calc.account.models import User

from config.models import BaseModel


class RouteShipment(models.TextChoices):
    CH_RU = 'CHINA-RUSSIA'
    CH_BY = 'CHINA-BELARUS'


class Shipment(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shipment',
    )

    number = models.CharField(
        max_length=30,
        verbose_name="Номер поставки"
    )

    route = models.CharField(
        choices=RouteShipment,
        verbose_name="Маршрут поставки"
    )

    status = models.CharField(
        max_length=30,
        verbose_name="Статус поставки"
    )

    note = models.CharField(
        max_length=255,
        verbose_name="Примечание",
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['number']
        db_table = 'shipment'
        verbose_name = "Поставка"
        verbose_name_plural = "Поставки"
