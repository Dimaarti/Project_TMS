from decimal import Decimal
from unittest.mock import MagicMock, patch

from django.test import TestCase

from china_calc.finance.calculators.shipment_cargo_calculator import (
    ShipmentCargoCalculator,
)


class TestShipmentCargoCalculator(TestCase):
    # проверка суммирования всех товаров
    def test_calculate_total_weight_and_volume(self):
        shipment = MagicMock()

        shipment.items.aggregate.return_value = {
            "total_weight": Decimal(10),
            "total_volume": Decimal("2.5"),
        }

        calculator = ShipmentCargoCalculator(shipment=shipment)

        result = calculator.calculate()

        self.assertEqual(result["weight"], Decimal(10))
        self.assertEqual(result["volume"], Decimal("2.5"))

    # проверка правильного объекта поставки
    @patch(
        "china_calc.finance.calculators."
        "shipment_cargo_calculator."
        "Shipment.objects.filter"
    )
    def test_applies_weight_and_volume_to_shipment(self, mocked_filter):
        shipment = MagicMock()
        shipment.pk = 19

        shipment.items.aggregate.return_value = {
            "total_weight": Decimal(10),
            "total_volume": Decimal("2.5"),
        }
        calculator = ShipmentCargoCalculator(shipment=shipment)

        result = calculator.apply()

        mocked_filter.assert_called_with(pk=19)
        mocked_filter.return_value.update.assert_called_with(
            weight=Decimal(10), volume=Decimal("2.5")
        )

        self.assertEqual(shipment.weight, Decimal(10))
        self.assertEqual(shipment.volume, Decimal("2.5"))
        self.assertEqual(result, {"weight": Decimal(10), "volume": Decimal("2.5")})

    # проверка поставки без товаров
    def test_returns_zero_when_shipment_has_no_items(self):
        shipment = MagicMock()

        shipment.items.aggregate.return_value = {
            "total_weight": Decimal(0),
            "total_volume": Decimal(0),
        }

        calculator = ShipmentCargoCalculator(shipment=shipment)

        result = calculator.calculate()

        self.assertEqual(result["weight"], Decimal(0))
        self.assertEqual(result["volume"], Decimal(0))
