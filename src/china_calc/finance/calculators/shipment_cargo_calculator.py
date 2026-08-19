from decimal import Decimal

from django.db.models import Sum

from china_calc.shipment.models import Shipment


class ShipmentCargoCalculator:
    def __init__(self, shipment: Shipment):
        self.shipment = shipment

    def calculate(self):
        """
        Общий вес и объем товаров поставки.
        """

        totals = self.shipment.items.aggregate(
            total_weight=Sum("weight", default=Decimal(0)),
            total_volume=Sum("volume", default=Decimal(0)),
        )

        return {
            "weight": totals["total_weight"],
            "volume": totals["total_volume"],
        }

    def apply(self):
        """
        Рассчитывает и записывает вес и объем в поставку.
        """

        totals = self.calculate()

        Shipment.objects.filter(
            pk=self.shipment.pk,
        ).update(
            weight=totals["weight"],
            volume=totals["volume"],
        )

        self.shipment.weight = totals["weight"]
        self.shipment.volume = totals["volume"]

        return totals
