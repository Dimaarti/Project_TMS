from decimal import Decimal

from django.test import TestCase

from china_calc.finance.calculators.price_cost_calculator import PriceCostCalculator


class TestPriceCostCalculator(TestCase):
    # тест правильного расчета
    def test_calculates_price_cost(self):
        purchase_cost = Decimal(1)
        logistics_cost = Decimal(9)
        expenses_cost = Decimal(1)

        result = PriceCostCalculator.calculate(
            purchase_cost=purchase_cost,
            logistics_cost=logistics_cost,
            expenses_cost=expenses_cost,
        )

        self.assertEqual(result, Decimal(11))

    # тесты введения неправильных данных
    def test_rejects_negative_purchase_cost(self):
        with self.assertRaisesRegex(
            ValueError, "Составляющие себестоимости не могут быть отрицательными"
        ):
            PriceCostCalculator.calculate(
                purchase_cost=Decimal(-1),
                logistics_cost=Decimal(1),
                expenses_cost=Decimal(1),
            )

    def test_rejects_negative_logistics_cost(self):
        with self.assertRaisesRegex(
            ValueError, "Составляющие себестоимости не могут быть отрицательными"
        ):
            PriceCostCalculator.calculate(
                purchase_cost=Decimal(1),
                logistics_cost=Decimal(-1),
                expenses_cost=Decimal(1),
            )

    def test_rejects_negative_expenses_cost(self):
        with self.assertRaisesRegex(
            ValueError, "Составляющие себестоимости не могут быть отрицательными"
        ):
            PriceCostCalculator.calculate(
                purchase_cost=Decimal(1),
                logistics_cost=Decimal(1),
                expenses_cost=Decimal(-1),
            )
