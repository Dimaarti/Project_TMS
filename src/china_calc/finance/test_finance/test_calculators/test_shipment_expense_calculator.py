from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import MagicMock

from django.test import TestCase

from china_calc.finance.calculators.shipment_expense_calculator import (
    ShipmentExpenseCalculator,
)
from config.model_choices import Currency, LogisticCalculationMethod, DeliveryRouteType


class TestShipmentExpenseCalculator(TestCase):
    def setUp(self):
        self.items = [
            SimpleNamespace(
                pk=1,
                client_id=1,
                weight=Decimal(2),
                volume=Decimal("0.1"),
            ),
            SimpleNamespace(
                pk=2,
                client_id=1,
                weight=Decimal(4),
                volume=Decimal("0.3"),
            ),
            SimpleNamespace(
                pk=3,
                client_id=2,
                weight=Decimal(6),
                volume=Decimal("0.5"),
            ),
        ]

    def build_shipment(self, expenses):
        shipment = MagicMock()
        shipment.pk = 10
        shipment.logistic_calculation_type = LogisticCalculationMethod.WEIGHT
        shipment.settlement_final_currency = Currency.BYN
        shipment.route_type = DeliveryRouteType.CHINA_BELARUS
        shipment.exchange_rate = SimpleNamespace()
        shipment.items.select_related.return_value.order_by.return_value = self.items
        shipment.expenses.select_related.return_value.order_by.return_value = expenses

        return shipment

    # основная проверка расходов
    def test_calculates_direct_and_common_expenses(self):
        expenses = [
            SimpleNamespace(
                item_id=1,
                item=SimpleNamespace(shipment_id=10),
                amount=Decimal(15),
                currency=Currency.BYN,
            ),
            SimpleNamespace(
                item_id=None,
                item=None,
                amount=Decimal(60),
                currency=Currency.BYN,
            ),
        ]

        shipment = self.build_shipment(expenses)

        result = ShipmentExpenseCalculator.calculate(shipment=shipment)

        self.assertEqual(result["direct_expenses_cost"], Decimal(15))
        self.assertEqual(result["common_expenses_cost"], Decimal(60))
        self.assertEqual(result["total_expenses_cost"], Decimal(75))

        first_item = result["items"][1]
        second_item = result["items"][2]
        third_item = result["items"][3]

        self.assertEqual(first_item["direct_expenses_cost"], Decimal(15))
        self.assertEqual(first_item["distributed_expenses_cost"], Decimal(10))
        self.assertEqual(first_item["total_expenses_cost"], Decimal(25))

        self.assertEqual(second_item["direct_expenses_cost"], Decimal(0))
        self.assertEqual(second_item["distributed_expenses_cost"], Decimal(20))
        self.assertEqual(second_item["total_expenses_cost"], Decimal(20))

        self.assertEqual(third_item["direct_expenses_cost"], Decimal(0))
        self.assertEqual(third_item["distributed_expenses_cost"], Decimal(30))
        self.assertEqual(third_item["total_expenses_cost"], Decimal(30))

        first_client = result["clients"][1]
        second_client = result["clients"][2]

        self.assertEqual(first_client["direct_expenses_cost"], Decimal(15))
        self.assertEqual(first_client["distributed_expenses_cost"], Decimal(30))
        self.assertEqual(first_client["total_expenses_cost"], Decimal(45))

        self.assertEqual(second_client["direct_expenses_cost"], Decimal(0))
        self.assertEqual(second_client["distributed_expenses_cost"], Decimal(30))
        self.assertEqual(second_client["total_expenses_cost"], Decimal(30))

        distributed_total = sum(
            (
                item_result["distributed_expenses_cost"]
                for item_result in result["items"].values()
            ),
            Decimal(0),
        )

        self.assertEqual(distributed_total, Decimal(60))

    # проверка поставки без расходов
    def test_returns_shipment_has_no_expenses(self):
        shipment = self.build_shipment(expenses=[])

        result = ShipmentExpenseCalculator.calculate(shipment=shipment)

        self.assertEqual(result["direct_expenses_cost"], Decimal(0))
        self.assertEqual(result["common_expenses_cost"], Decimal(0))
        self.assertEqual(result["total_expenses_cost"], Decimal(0))

        for item_result in result["items"].values():
            self.assertEqual(item_result["total_expenses_cost"], Decimal(0))

    # проверка поставки без товаров
    def test_returns_shipment_has_no_items(self):
        shipment = self.build_shipment(expenses=[])
        shipment.items.select_related.return_value.order_by.return_value = []

        with self.assertRaisesRegex(ValueError, "В поставке нет товаров"):
            ShipmentExpenseCalculator.calculate(shipment=shipment)

    # проверка привязки товара расхода к другой поставке
    def test_rejects_expense_for_item_from_another_shipment(self):
        expenses = [
            SimpleNamespace(
                item_id=333,
                item=SimpleNamespace(shipment_id=100),
                amount=Decimal(15),
                currency=Currency.BYN,
            )
        ]

        shipment = self.build_shipment(expenses=expenses)

        with self.assertRaisesRegex(
            ValueError, "Товар расхода не принадлежит этой поставке"
        ):
            ShipmentExpenseCalculator.calculate(shipment=shipment)

    # проверка отрицательной суммы расхода
    def test_rejects_negative_expense_amount(self):
        expenses = [
            SimpleNamespace(
                item_id=None,
                item=None,
                amount=Decimal(-1),
                currency=Currency.BYN,
            )
        ]

        shipment = self.build_shipment(expenses=expenses)

        with self.assertRaisesRegex(
            ValueError, "Сумма расхода не может быть отрицательной"
        ):
            ShipmentExpenseCalculator.calculate(shipment=shipment)
