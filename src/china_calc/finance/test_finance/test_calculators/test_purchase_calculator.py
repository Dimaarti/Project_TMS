from decimal import Decimal
from types import SimpleNamespace

from django.test import TestCase

from china_calc.finance.calculators.purchase_calculator import PurchaseCalculator
from config.model_choices import Currency


class TestPurchaseCalculator(TestCase):
    def setUp(self):
        self.shipment = SimpleNamespace(
            settlement_final_currency=Currency.BYN,
            exchange_rate=SimpleNamespace(
                cny_to_byn=Decimal("0.45"),
                cny_to_byn_client=Decimal("0.50"),
            ),
        )

    # проверка стоимости одного товара
    def test_calculate_item_purchase_cost(self):
        item = SimpleNamespace(
            price=Decimal("100"),
            quantity=3,
            price_currency=Currency.CNY,
        )

        result = PurchaseCalculator.calculate_item(
            item=item,
            shipment=self.shipment,
        )

        self.assertEqual(result, Decimal("135"))

    # проверка стоимости товара по клиентскому курсу
    def test_calculate_item_client_purchase_cost(self):
        item = SimpleNamespace(
            price=Decimal("100"),
            quantity=3,
            price_currency=Currency.CNY,
        )

        result = PurchaseCalculator.calculate_item(
            item=item,
            shipment=self.shipment,
            for_client=True,
        )

        self.assertEqual(result, Decimal("150"))

    # проверка стоимости нескольких товаров
    def test_calculate_multiple_items(self):
        items = [
            SimpleNamespace(
                price=Decimal("100"),
                quantity=3,
                price_currency=Currency.CNY,
            ),
            SimpleNamespace(
                price=Decimal("200"),
                quantity=1,
                price_currency=Currency.CNY,
            ),
        ]

        result = PurchaseCalculator.calculate_items(
            items=items,
            shipment=self.shipment,
        )

        self.assertEqual(result, Decimal("225"))

    # проверка пустого списка товаров
    def test_list_items_zero(self):
        result = PurchaseCalculator.calculate_items(
            items=[],
            shipment=self.shipment,
        )

        self.assertEqual(result, Decimal("0"))

    # проверка нулевой цены
    def test_price_zero(self):
        item = SimpleNamespace(
            price=Decimal("0"),
            quantity=1,
            price_currency=Currency.CNY,
        )

        result = PurchaseCalculator.calculate_item(
            item=item,
            shipment=self.shipment,
        )

        self.assertEqual(result, Decimal("0"))

    # проверка отрицательной цены
    def test_rejects_negative_price(self):
        item = SimpleNamespace(
            price=Decimal("-100"),
            quantity=1,
            price_currency=Currency.CNY,
        )

        with self.assertRaisesRegex(
            ValueError, "Цена товара не может быть отрицательной"
        ):
            PurchaseCalculator.calculate_item(
                item=item,
                shipment=self.shipment,
            )

    # проверка отрицательного или нулевого количества
    def test_rejects_negative_or_zero_quantity(self):
        item = SimpleNamespace(
            price=Decimal("100"),
            quantity=0,
            price_currency=Currency.CNY,
        )

        with self.assertRaisesRegex(
            ValueError, "Количество товара должно быть больше 0"
        ):
            PurchaseCalculator.calculate_item(
                item=item,
                shipment=self.shipment,
            )
