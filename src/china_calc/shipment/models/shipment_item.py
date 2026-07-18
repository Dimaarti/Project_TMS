from django.db import models




class ShipmentItem(models.Model):
    shipment = models.ForeignKey(
        to='Shipment',
        on_delete=models.CASCADE,
        related_name='item',
    )

    client = models.ForeignKey(
        to='client.Client',
        on_delete=models.CASCADE,
        related_name='item',
    )

    product = models.ForeignKey(
        to='Product',
        on_delete=models.CASCADE,
        related_name='item',
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    volume = models.DecimalField(
        max_digits=10,
        decimal_places=4,
    )

    inspection_cost = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
    )

    photo_report_cost = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
    )

    packaging_cost = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        ordering = ['-quantity', '-price']
        verbose_name = "Товар для отправки"
        verbose_name_plural = "Товары для отправки"

    def __str__(self):
        return self.product.name