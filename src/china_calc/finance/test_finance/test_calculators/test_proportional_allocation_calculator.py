from decimal import Decimal
from types import SimpleNamespace

from django.test import TestCase

from china_calc.finance.calculators.proportional_allocation_calculator import (
    ProportionalAllocationCalculator,
)


class TestProportionalAllocationCalculator(TestCase):
    def setUp(self):
        self.items = [
            SimpleNamespace(pk=1),
            SimpleNamespace(pk=2),
        ]

    # проверка обычного распределения
    def test_allocates_amount_proportionally(self):
        result = ProportionalAllocationCalculator.allocate(
            items=self.items,
            total_amount=Decimal("100"),
            basis_item={
                1: Decimal("20"),
                2: Decimal("30"),
            },
            total_basis=Decimal("50"),
        )

        self.assertEqual(
            result,
            {
                1: Decimal("40"),
                2: Decimal("60"),
            },
        )

    # проверка сохранения общей суммы
    def test_allocated_sum_totals_amount(self):
        items = [
            SimpleNamespace(pk=1),
            SimpleNamespace(pk=2),
            SimpleNamespace(pk=3),
        ]

        result = ProportionalAllocationCalculator.allocate(
            items=items,
            total_amount=Decimal("100"),
            basis_item={
                1: Decimal("10"),
                2: Decimal("10"),
                3: Decimal("10"),
            },
            total_basis=Decimal("30"),
        )

        self.assertEqual(sum(result.values(), Decimal("0")), Decimal("100"))

    # проверка конкретных дробных долей
    def test_allocated_equal_parts(self):
        items = [
            SimpleNamespace(pk=1),
            SimpleNamespace(pk=2),
            SimpleNamespace(pk=3),
        ]

        result = ProportionalAllocationCalculator.allocate(
            items=items,
            total_amount=Decimal("100"),
            basis_item={
                1: Decimal("1"),
                2: Decimal("1"),
                3: Decimal("1"),
            },
            total_basis=Decimal("3"),
        )

        expected_parts = Decimal("100") / Decimal("3")

        self.assertEqual(result[1], expected_parts)
        self.assertEqual(result[2], expected_parts)
        self.assertEqual(result[3], Decimal("100") - expected_parts * 2)

    # проверка нулевой суммы распределения
    def test_allocated_zero_amount(self):
        result = ProportionalAllocationCalculator.allocate(
            items=self.items,
            total_amount=Decimal("0"),
            basis_item={
                1: Decimal("1"),
                2: Decimal("3"),
            },
            total_basis=Decimal("4"),
        )

        self.assertEqual(
            result,
            {
                1: Decimal("0"),
                2: Decimal("0"),
            },
        )

    # проверка пустого списка товаров (сначала проверяется наличие)
    def test_returns_empy_dict(self):
        result = ProportionalAllocationCalculator.allocate(
            items=[],
            total_amount=Decimal("100"),
            basis_item={},
            total_basis=Decimal("0"),
        )

        self.assertEqual(result, {})

    # проверка отрицательной общей суммы
    def test_rejects_negative_total_amount(self):
        with self.assertRaisesRegex(
            ValueError, "Распределяемая сумма не может быть отрицательной"
        ):
            result = ProportionalAllocationCalculator.allocate(
                items=self.items,
                total_amount=Decimal("-100"""),
                basis_item={
                    1: Decimal("1"),
                    2: Decimal("1"),
                },
                total_basis=Decimal("2"),
            )

    # проверка нулевой базы распределения
    def test_zero_total_basis(self):
        with self.assertRaisesRegex(
            ValueError, "Общая база распределения должна быть больше 0"
        ):
            result = ProportionalAllocationCalculator.allocate(
                items=self.items,
                total_amount=Decimal("100"),
                basis_item={
                    1: Decimal("0"),
                    2: Decimal("0"),
                },
                total_basis=Decimal("0"),
            )

    # проверка отсутствия базы товара
    def test_none_basis_item(self):
        with self.assertRaisesRegex(
            ValueError, "Для товара не указана база распределения"
        ):
            result = ProportionalAllocationCalculator.allocate(
                items=self.items,
                total_amount=Decimal("100"),
                basis_item={
                    1: Decimal("1"),
                    2: None,
                },
                total_basis=Decimal("1"),
            )

    # проверка отрицательной базы товаров
    def test_rejects_negative_basis_item(self):
        with self.assertRaisesRegex(
            ValueError, "База распределения товаров не может быть отрицательной"
        ):
            result = ProportionalAllocationCalculator.allocate(
                items=self.items,
                total_amount=Decimal("100"),
                basis_item={
                    1: Decimal("-1"),
                    2: Decimal("2"),
                },
                total_basis=Decimal("1"),
            )
