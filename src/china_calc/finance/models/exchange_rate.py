from django.db import models
from config.models import BaseModel


class ExchangeRate(BaseModel):
    date = models.DateField(
        verbose_name='Дата'
    )

    cny_to_byn = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Курс СNY/BYN'
    )

    cny_to_rub = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Курс СNY/RUB'
    )

    usd_to_byn = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Курс USD/BYN'
    )

    usd_to_rub = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Курс USD/RUB'
    )

    rub_to_byn = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Курс RUB/BYN'
    )

    class Meta:
        verbose_name_plural = 'Обменные курсы'

    def __str__(self):
        return f'Обменный курс на дату - {self.date}'
