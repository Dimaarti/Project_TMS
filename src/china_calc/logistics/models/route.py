from django.db import models

from config.base_models import BaseModel
from config.model_choices import TransportType


class Route(BaseModel):
    dispatch_country = models.CharField(
        max_length=100, verbose_name="Страна отправления"
    )

    destination_country = models.CharField(
        max_length=100, verbose_name="Страна назначения"
    )

    transport_type = models.CharField(
        max_length=100, choices=TransportType.choices, verbose_name="Тип транспорта"
    )

    is_active = models.BooleanField(default=True, verbose_name="Активный маршрут")

    class Meta:
        ordering = ["dispatch_country", "destination_country", "transport_type"]
        verbose_name = "Маршрут доставки"
        verbose_name_plural = "Маршруты доставки"

        constraints = [
            models.UniqueConstraint(
                fields=["dispatch_country", "destination_country", "transport_type"],
                name="unique_country_and_transport_type",
            )
        ]

    def __str__(self):
        return (
            f"Маршрут {self.dispatch_country} - "
            f"{self.destination_country}, "
            f"{self.get_transport_type_display()}"
        )
