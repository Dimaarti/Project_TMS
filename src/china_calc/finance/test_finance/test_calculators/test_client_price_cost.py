from decimal import Decimal

from django.test import TestCase

from china_calc.finance.calculators.client_price_cost_calculator import (
    ClientPriceCostCalculator,
)


class TestClientPriceCostCalculator(TestCase):
    # тест правильного расчета
    def test_calculates_client_price_cost(self):
        client_purchase_cost = Decimal(1)
        logistics_cost = Decimal(1)
        expenses_cost = Decimal(1)
        buyer_commission_cost = Decimal(1)

        result = ClientPriceCostCalculator.calculate(
            client_purchase_cost=client_purchase_cost,
            logistics_cost=logistics_cost,
            expenses_cost=expenses_cost,
            buyer_commission_cost=buyer_commission_cost,
        )

        self.assertEqual(result, Decimal(1))

    # тесты введения неправильных данных
    def test_rejects_negative_client_purchase_cost(self):
        with self.assertRaisesRegex(
            ValueError, "Составляющие клиентской стоимости не могут быть отрицательными"
        ):
            ClientPriceCostCalculator.calculate(
                client_purchase_cost=Decimal(-1),
                logistics_cost=Decimal(1),
                expenses_cost=Decimal(1),
                buyer_commission_cost=Decimal(1),
            )

    def test_rejects_negative_logistics_cost(self):
        with self.assertRaisesRegex(
            ValueError, "Составляющие клиентской стоимости не могут быть отрицательными"
        ):
            ClientPriceCostCalculator.calculate(
                client_purchase_cost=Decimal(1),
                logistics_cost=Decimal(-1),
                expenses_cost=Decimal(1),
                buyer_commission_cost=Decimal(1),
            )

    def test_rejects_negative_expenses_cost(self):
        with self.assertRaisesRegex(
            ValueError, "Составляющие клиентской стоимости не могут быть отрицательными"
        ):
            ClientPriceCostCalculator.calculate(
                client_purchase_cost=Decimal(1),
                logistics_cost=Decimal(1),
                expenses_cost=Decimal(-1),
                buyer_commission_cost=Decimal(1),
            )

    def test_rejects_negative_buyer_commission_cost(self):
        with self.assertRaisesRegex(
            ValueError, "Составляющие клиентской стоимости не могут быть отрицательными"
        ):
            ClientPriceCostCalculator.calculate(
                client_purchase_cost=Decimal(1),
                logistics_cost=Decimal(1),
                expenses_cost=Decimal(1),
                buyer_commission_cost=Decimal(-1),
            )
