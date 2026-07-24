from django.db import models

class TransportType(models.TextChoices):
    AIR = 'air', 'Авиационный'
    AUTO = 'auto', 'Автомобильный'
    SEA = 'sea', 'Морской'
    RAIL = 'rail','Железнодорожный'


class Route(models.Model):
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
        return f'Маршрут[{self.name}, {self.transport_type}]'