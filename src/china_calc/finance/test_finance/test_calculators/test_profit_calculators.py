from decimal import Decimal

from django.test import TestCase

from china_calc.finance.calculators.profit_calculate import ProfitCostCalculator


class TestProfitCalculator(TestCase):
    # проверка расчета прибыли
    def test_calculate_profit(self):
        result = ProfitCostCalculator.calculate(
            client_price_cost=Decimal("10"),
            price_cost=Decimal("5"),
        )

        self.assertEqual(result, Decimal("5"))

    # проверка отсутствия прибыли
    def test_zero_profit(self):
        result = ProfitCostCalculator.calculate(
            client_price_cost=Decimal("5"),
            price_cost=Decimal("5"),
        )

        self.assertEqual(result, Decimal("0"))

    # проверка убытка
    def test_negative_profit(self):
        result = ProfitCostCalculator.calculate(
            client_price_cost=Decimal("20"),
            price_cost=Decimal("30"),
        )

        self.assertEqual(result, Decimal("-10"))

    # проверка отрицательной клиентской стоимости (должна быть положительной)
    def test_rejects_negative_client_price_cost(self):
        with self.assertRaisesRegex(
            ValueError, "Клиентская стоимость не может быть отрицательной"
        ):
            ProfitCostCalculator.calculate(
                client_price_cost=Decimal("-10"),
                price_cost=Decimal("5"),
            )

    # проверка отрицательной себестоимости (должна быть положительной)
    def test_rejects_negative_price_cost(self):
        with self.assertRaisesRegex(
            ValueError, "Себестоимость не может быть отрицательной"
        ):
            ProfitCostCalculator.calculate(
                client_price_cost=Decimal("10"),
                price_cost=Decimal("-5"),
            )
