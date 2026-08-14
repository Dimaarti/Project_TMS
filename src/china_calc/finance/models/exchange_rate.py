from django.db import models

from config.base_models import BaseModel


class ExchangeRate(BaseModel):
    user = models.ForeignKey(
        to="account.User",
        on_delete=models.CASCADE,
        related_name="exchange_rates",
        verbose_name="Пользователь",
    )

    date = models.DateField(verbose_name="Дата")

    cny_to_byn = models.DecimalField(
        max_digits=10, decimal_places=4, verbose_name="Курс СNY/BYN - себестоимость"
    )

    cny_to_byn_client = models.DecimalField(
        max_digits=10, decimal_places=4, verbose_name="Курс СNY/BYN - для клиента"
    )

    cny_to_rub = models.DecimalField(
        max_digits=10, decimal_places=4, verbose_name="Курс СNY/RUB - себестоимость"
    )

    cny_to_rub_client = models.DecimalField(
        max_digits=10, decimal_places=4, verbose_name="Курс СNY/RUB - для клиента"
    )

    usd_to_byn = models.DecimalField(
        max_digits=10, decimal_places=4, verbose_name="Курс USD/BYN - себестоимость"
    )

    usd_to_byn_client = models.DecimalField(
        max_digits=10, decimal_places=4, verbose_name="Курс USD/BYN - для клиента"
    )

    usd_to_rub = models.DecimalField(
        max_digits=10, decimal_places=4, verbose_name="Курс USD/RUB - себестоимость"
    )

    usd_to_rub_client = models.DecimalField(
        max_digits=10, decimal_places=4, verbose_name="Курс USD/RUB - для клиента"
    )

    rub_to_byn = models.DecimalField(
        max_digits=10, decimal_places=4, verbose_name="Курс RUB/BYN - себестоимость"
    )

    rub_to_byn_client = models.DecimalField(
        max_digits=10, decimal_places=4, verbose_name="Курс RUB/BYN - для клиента"
    )

    class Meta:
        ordering = ["-date"]
        verbose_name = "Обменный курс"
        verbose_name_plural = "Обменные курсы"

    def __str__(self):
        return f"Обменные курсы на - {self.date}"
