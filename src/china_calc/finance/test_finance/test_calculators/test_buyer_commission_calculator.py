from decimal import Decimal
from unittest import TestCase

from china_calc.finance.calculators.buyer_commission_calculator import (
    BuyerCommissionCalculator,
)


class TestBuyerCommissionCalculator(TestCase):
    # проверка расчета комиссии
    def test_calculate_commission(self):
        result = BuyerCommissionCalculator.calculate_amount(
            client_purchase_cost=Decimal("100"),
            commission_percent=Decimal("10"),
        )

        self.assertEqual(result, Decimal("10"))

    # проверка дробного процента
    def test_float_commission(self):
        result = BuyerCommissionCalculator.calculate_amount(
            client_purchase_cost=Decimal("100"),
            commission_percent=Decimal("5.5"),
        )

        self.assertEqual(result, Decimal("5.5"))

    # проверка нулевой комиссии
    def test_zero_commission(self):
        result = BuyerCommissionCalculator.calculate_amount(
            client_purchase_cost=Decimal("100"),
            commission_percent=Decimal("0"),
        )

        self.assertEqual(result, Decimal("0"))

    # проверка отрицательной стоимости клиента
    def test_rejects_negative_client_price_cost(self):
        with self.assertRaisesRegex(
            ValueError,
            "Стоимость товаров клиента не может быть отрицательной",
        ):
            BuyerCommissionCalculator.calculate_amount(
                client_purchase_cost=Decimal("-100"),
                commission_percent=Decimal("5"),
            )

    # проверка отрицательного процента
    def test_rejects_negative_commission_percent(self):
        with self.assertRaisesRegex(
            ValueError, "Процент комиссии не может быть отрицательным"
        ):
            BuyerCommissionCalculator.calculate_amount(
                client_purchase_cost=Decimal("100"),
                commission_percent=Decimal("-5"),
            )

    # проверка, процент больше 100
    def test_commission_percent_great_one_hundred(self):
        with self.assertRaisesRegex(
            ValueError, "Процент комиссии не может быть больше 100"
        ):
            BuyerCommissionCalculator.calculate_amount(
                client_purchase_cost=Decimal("100"),
                commission_percent=Decimal("102"),
            )
