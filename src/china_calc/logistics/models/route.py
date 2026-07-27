from django.db import models

from config.model_choices import TransportType
from config.models import BaseModel


class Route(BaseModel):
    name = models.CharField(
        max_length=100,
        verbose_name='Название маршрута'
    )

    dispatch_country = models.CharField(
        max_length=100,
        verbose_name='Страна отправления'
    )

    destination_country = models.CharField(
        max_length=100,
        verbose_name='Страна назначения'
    )

    transport_type = models.CharField(
        max_length=100,
        choices=TransportType.choices,
        verbose_name='Тип транспорта'
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Маршруты доставки'

    def __str__(self):
        return (f'Маршрут[{self.name} -, '
                f'{self.transport_type}]')
