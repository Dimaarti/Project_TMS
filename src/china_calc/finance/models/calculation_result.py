from django.db import models

from config.models import BaseModel


class CalculationResult(BaseModel):
    shipment = models.OneToOneField(
        to='shipment.Shipment',
        on_delete=models.CASCADE,
        related_name='calculation_result',
        verbose_name='Поставка'
    )

    exchange_rate = models.ForeignKey(
        to='ExchangeRate',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='calculation_result',
        verbose_name='Обменный курс',
    )

    base_currency = models.CharField(
        max_length=3,
        default='CNY',
        verbose_name='Валюта базовая'
    )

    counter_currency = models.CharField(
        max_length=5,
        verbose_name='Валюта котировки'
    )

    purchase_cost = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
        verbose_name='Стоимость товара'
    )

    logistics_cost = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
        verbose_name='Логистические расходы'
    )

    duty_cost = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
        verbose_name='Расчет пошлины'
    )

    buyer_commission_cost = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
        verbose_name='Расчет комиссии байера'
    )

    price_cost = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
        verbose_name='Расчет себестоимости'
    )

    profit_cost = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
        verbose_name='Прибыль'
    )

    add_services = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        default=0,
        verbose_name='Дополнительные услуги',
    )

    class Meta:
        verbose_name_plural = 'Результаты расчетов'

    def __str__(self):
        return f'Расчет поставки {self.shipment.number}'

