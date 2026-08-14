from decimal import Decimal
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import MagicMock, patch

from china_calc.finance.calculators.logistic_allocation_calculator import LogisticAllocationCalculator
from config.model_choices import LogisticCalculationMethod


class TestLogisticAllocationCalculator(TestCase):
    def setUp(self):
        self.items = [
            SimpleNamespace(
                pk=1,
                client_id=1,
                weight=Decimal('1'),
                volume=Decimal('0.1'),
            ),
            SimpleNamespace(
                pk=2,
                client_id=1,
                weight=Decimal('2'),
                volume=Decimal('0.3'),
            ),
            SimpleNamespace(
                pk=3,
                client_id=2,
                weight=Decimal('3'),
                volume=Decimal('0.5'),
            )
        ]

    # создание поддельной поставки, MagicMock имитирует цепочку создания
    def build_shipment(self, calculation_type):
        shipment = MagicMock()
        shipment.logistic_calculation_type = calculation_type
        shipment.items.select_related.return_value.order_by.return_value = self.items

        return shipment

    # проверка распределения по весу (patch заменяет вызов LogisticCalculator)
    @patch(
        "china_calc.finance.calculators."
        "logistic_allocation_calculator."
        "LogisticCalculator.calculate"
    )
    def test_allocates_logistic_by_weight(self, mock_calculate):
        mock_calculate.return_value = Decimal('100')

        shipment = self.build_shipment(LogisticCalculationMethod.WEIGHT)

        result = LogisticAllocationCalculator.calculate(shipment=shipment)

        expected_first_cost = Decimal('100') * Decimal('1') / Decimal('6')
        expected_second_cost = Decimal('100') * Decimal('2') / Decimal('6')

        self.assertEqual(result.logistics_cost, Decimal('100'))
        self.assertEqual(result.total_basis, Decimal('6'))
        self.assertEqual(result.items[1].logistics_cost, expected_first_cost)
        self.assertEqual(result.items[2].logistics_cost, expected_second_cost)
        self.assertEqual(result.items[3].logistics_cost, Decimal('100') - expected_first_cost - expected_second_cost)
        self.assertEqual(
            sum(
                (
                    allocation.logistics_cost
                    for allocation in result.items.values()
                ),
                Decimal("0"),
            ),
            Decimal("100")
        )

    # проверка поставки без товаров
    def test_rejects_items_in_shipment(self):
        shipment = MagicMock()
        shipment.items.select_related.return_value.order_by.return_value = []

        with self.assertRaisesRegex(
                ValueError,
                "Отсутствуют товары в поставке"
        ):
            LogisticAllocationCalculator.calculate(shipment=shipment)

    # проверка нулевой базы распределения
    @patch(
        "china_calc.finance.calculators."
        "logistic_allocation_calculator."
        "LogisticCalculator.calculate"
    )
    def test_rejects_zero_total_basis(self, mock_calculate):
        mock_calculate.return_value = Decimal('100')

        items = [
            SimpleNamespace(
                pk=1,
                client_id=3,
                weight=Decimal('0'),
                volume=Decimal('0'),
            ),
            SimpleNamespace(
                pk=2,
                client_id=4,
                weight=Decimal('0'),
                volume=Decimal('0'),
            )
        ]

        shipment = MagicMock()
        shipment.logistic_calculation_type = LogisticCalculationMethod.WEIGHT
        shipment.items.select_related.return_value.order_by.return_value = items

        with self.assertRaisesRegex(
            ValueError,
            "Невозможно распределить логистику"
        ):
            LogisticAllocationCalculator.calculate(shipment=shipment)

    # проверка неизвестного способа распределения
    def test_unknown_calculation_method(self):
        shipment = SimpleNamespace(
            logistic_calculation_type="unknown",
        )

        with self.assertRaisesRegex(
            ValueError,
            "Неизвестный способ распределения"
        ):
            LogisticAllocationCalculator.get_basis_item(
                shipment=shipment,
                items=self.items
            )


