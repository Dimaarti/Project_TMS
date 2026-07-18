from django.db import models

class ExpenseType(models.TextChoices):
    TRANSPORT = 'transport', 'Международная доставка'
    TC = 'transport_company', 'Доставка транспортной компанией'
    INSURANCE = 'insurance', 'Страхование'
    LOADING = 'loading','Загрузка'
    UNLOADING = 'unloading','Отгрузка'
    PACKAGING = 'packaging','Усиленная упаковка'
    PHOTO = 'photo_report','Фотоотчет'
    INSPECTION = 'inspection','Проверка'
    CUSTOMS = 'customs','Таможенные расходы'
    OTHER = 'other','Прочее'

class Currency(models.TextChoices):
    CNY = 'CNY'
    RUB = 'RUB'
    BYN = 'BYN'

class ShipmentExpense(models.Model):
    shipment = models.ForeignKey(
        to='Shipment',
        on_delete=models.CASCADE,
        related_name='expense',
    )

    expense_type = models.CharField(
        max_length=40,
        choices=ExpenseType.choices,
        verbose_name='Тип расходов'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма'
    )

    currency = models.CharField(
        max_length=10,
        choices=Currency.choices,
        verbose_name='Валюта'
    )

    class Meta:
        ordering = ['-amount']
        verbose_name_plural = 'Расходы'

    def __str__(self):
        return self.expense_type

