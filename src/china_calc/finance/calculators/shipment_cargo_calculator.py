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

        box_weight = getattr(self.shipment, "box_weight", Decimal(0)) or Decimal(0)

        total_weight_with_box = totals["weight"] + box_weight

        Shipment.objects.filter(
            pk=self.shipment.pk,
        ).update(
            weight=total_weight_with_box,
            volume=totals["volume"],
        )

        self.shipment.weight = total_weight_with_box
        self.shipment.volume = totals["volume"]

        return {"weight": total_weight_with_box, "volume": totals["volume"]}
