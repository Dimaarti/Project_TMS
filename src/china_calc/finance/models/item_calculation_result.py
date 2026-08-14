from django.db import models

from config.base_models import BaseModel


class ItemCalculationResult(BaseModel):
    client_result = models.ForeignKey(
        to="ClientCalculationResult",
        on_delete=models.CASCADE,
        related_name="item_results",
        verbose_name="Расчет клиентов",
    )

    item = models.ForeignKey(
        to="shipment.ShipmentItem",
        on_delete=models.CASCADE,
        related_name="item_calculation_results",
        verbose_name="Товар",
    )

    purchase_cost = models.DecimalField(
        max_digits=14, decimal_places=2, default=0, verbose_name="Себестоимость товара"
    )

    client_purchase_cost = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
        verbose_name="Стоимость товара для клиентов",
    )

    allocation_basis = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
        verbose_name="Вес или объем для распределения",
    )

    allocation_ratio = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
        verbose_name="Доля товара в поставке",
    )

    logistics_cost = models.DecimalField(
        max_digits=14, decimal_places=2, default=0, verbose_name="Доля логистики товара"
    )

    direct_expenses_cost = models.DecimalField(
        max_digits=14, decimal_places=2, default=0, verbose_name="Прямые расходы товара"
    )

    distributed_expenses_cost = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
        verbose_name="Распределенные общие расходы",
    )

    total_cost = models.DecimalField(
        max_digits=14, decimal_places=2, default=0, verbose_name="Итого по товару"
    )

    class Meta:
        ordering = ["item__name"]
        verbose_name = "Результат расчета товара"
        verbose_name_plural = "Результаты расчетов по товарам"

    def __str__(self):
        return self.item.name
